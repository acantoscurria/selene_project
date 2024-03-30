import logging
from fastapi import APIRouter, Depends, HTTPException, Security, status, Response
from sqlmodel import Session, select
from app.api.v1.authentication import token_decode
from app.models.invites import Invites
from app.models.users import Users
from app.schemas.invites import InvitesByDniSchema, InvitesResponseSchema, InvitesCreateSchema, InvitesUpdateSchema
from app.core.database import get_session
from fastapi import Body

from app.schemas.users import UsersCreateSchema, UsersResponseSchema

router = APIRouter()

# Configura el registrador
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@router.post("/create_user", status_code=status.HTTP_201_CREATED, response_model=UsersResponseSchema)
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
    invite_exists = db.exec(select(Invites).where(Invites.id == new_user.invite_id)).first()

    if invite_exists.user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario ya está registrado"
        )

    user_data = new_user.model_dump()
    db_user = Users(**user_data)
    db_user.hash_password()
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"User created with ID: {db_user.id}, and values: {db_user}")
    return db_user


@router.get("/invite_by_dni/{dni_invite}",response_model=InvitesByDniSchema)
def get_invite_by_dni(
    dni_invite: str,
    db: Session = Depends(get_session)
    ):
    statement = select(Invites).where(Invites.dni == dni_invite)
    result = db.exec(statement)
    db_invite = result.first()
    if not db_invite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invitado no encontrado"
        )
    return db_invite


@router.get("/get_info_user", response_model=UsersResponseSchema)
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