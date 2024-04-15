from datetime import timedelta
import logging
from fastapi import APIRouter, Depends, HTTPException, Security, status, Response
from sqlmodel import Session, select
from app.api.v1.authentication import create_access_token, token_decode
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.models.invites import Invites
from app.models.users import Users
from app.schemas.common_users import CommonUserResponseSchema
from app.schemas.invites import  InvitesResponseSchema, InvitesCreateSchema, InvitesUpdateSchema
from app.core.database import get_session
from fastapi import Body

from app.schemas.users import UsersCreateSchema, UsersResponseCreateSchema, UsersResponseSchema

router = APIRouter()

# Configura el registrador
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@router.post("/create_user", status_code=status.HTTP_201_CREATED, response_model=UsersResponseCreateSchema)
def create_user(
    new_user: UsersCreateSchema, 
    db: Session = Depends(get_session)
    ):
    logger.info(f"Creating user with data: {new_user.model_dump()}")
    user_exists = db.exec(select(Users).where(Users.email == new_user.email)).first()
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario ya existe"
        )
    
    statement = select(Invites)

    invite_exists=db.exec(statement.where(Invites.phone_number == new_user.phone_number)).first()

    if not invite_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invitado no encontrado"
        )
    elif invite_exists.user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario ya está registrado"
        )

    user_data = new_user.model_dump()
    db_user = Users(**user_data)
    db_user.hash_password()
    db_user.invite = invite_exists
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"User created with ID: {db_user.id}, and values: {db_user}")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={
            "sub": str(db_user.id),
            "scopes":["invite"],
            "is_admin": db_user.is_admin,
            }, expires_delta=access_token_expires
    )
    res = {
        "user": db_user,
        "access_token": access_token,
        "token_type": "bearer",
    }
    return res



@router.get("/get_info_user", response_model=CommonUserResponseSchema)
def get_info_user(
    user = Security(token_decode,scopes=["invite"]),
    db: Session = Depends(get_session)
    ):
    
    logger.info(f"Getting user with ID: {user}")
    
    statement = select(Users).where(
        Users.id == user.get("sub"),
        Users.is_active == True,
        )
    result = db.exec(statement)
    db_user = result.first()
    logger.info(f"Getting user data: {db_user}")
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return db_user