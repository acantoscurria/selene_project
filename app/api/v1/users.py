from datetime import timedelta
import logging
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Security, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from app.api.v1.authentication import ACCESS_TOKEN_EXPIRE_MINUTES, TokenResponseSchema, create_access_token, token_decode, verify_password
from app.core.config import DEBUG
from app.models.invites import Invites
from app.models.users import Users
from app.schemas.users import UsersAdminCreateSchema, UsersCreateSchema, UserUpdateSchema, UserLoginSchema, UsersResponseSchema
from app.core.database import get_session
from fastapi import Body

router = APIRouter()

# Configura el registrador
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@router.post(
    "/token", status_code=status.HTTP_200_OK, response_model=TokenResponseSchema
)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_session),
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = select(Users).where(
        Users.email == form_data.username,
        Users.is_active == True,
    )
    user = db.exec(user).first()

    if not user:
        raise credentials_exception
    if not verify_password(form_data.password, user.password):
        raise credentials_exception

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    if user.is_admin:
        scope= "admin"
    else:
        scope= "invite"

    access_token = create_access_token(
        data={"sub": str(user.id),"scopes":[scope]}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/admin_user", status_code=status.HTTP_201_CREATED, response_model=UsersResponseSchema)
def create_admin_user(
    new_user: UsersAdminCreateSchema,
    db: Session = Depends(get_session)
    ):
    logger.info(f"Creating admin user with data: {new_user.model_dump()}")

    user_data = new_user.model_dump()
    db_user = Users(**user_data)
    db_user.hash_password()
    db_user.is_admin = True
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"User created with ID: {db_user.id}, and values: {db_user}")
    return db_user

@router.get("/{user_id}", response_model=UsersResponseSchema)
def get_user(
    user_id: int, 
    user = Security(token_decode,scopes=["admin"]),
    db: Session = Depends(get_session)):
    logger.info(f"Getting user with ID: {user_id}")
    
    statement = select(Users).where(
        Users.id == user_id,
        Users.is_active == True,
        )
    result = db.exec(statement)
    db_user = result.first()
    logger.info(f"Getting user data: {db_user}")
    if not db_user:
        logger.error(f"User with ID: {user_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return db_user


@router.get("/", response_model=list[UsersResponseSchema])
def get_users(
        user = Security(token_decode,scopes=["admin"]),
        db: Session = Depends(get_session)
    ):
    statement = select(Users).where(Users.is_active == True)
    result = db.exec(statement)
    db_users = result.all()
    return db_users


@router.patch("/{user_id}", response_model=UsersResponseSchema)
def update_user(
    user_id: int,
    user_data: UserUpdateSchema, 
    user = Security(token_decode,scopes=["admin"]),
    db: Session = Depends(get_session)):
    statement = select(Users).where(Users.id == user_id)
    result = db.exec(statement)
    db_user = result.first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    update_data = user_data.model_dump(exclude_unset=True)
    db_user.sqlmodel_update(update_data)
    if db_user.password:
        db_user.hash_password()
    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    user = Security(token_decode,scopes=["admin"]),
    db: Session = Depends(get_session)
    ):
    statement = select(Users).where(Users.id == user_id)
    result = db.exec(statement)
    db_user = result.first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    db.delete(db_user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
