from datetime import timedelta
import logging
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlmodel import Session, select
from app.api.v1.authentication import ACCESS_TOKEN_EXPIRE_MINUTES, TokenResponseSchema, create_access_token, verify_password
from app.models.guests import Guests
from app.schemas.guests import GuestsResponseSchema, GuestsCreateSchema, GuestsUpdateSchema
from app.models.users import Users
from app.core.database import get_session
from fastapi import Body

router = APIRouter()

# Configura el registrador
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@router.post(
    "/token", status_code=status.HTTP_200_OK, response_model=TokenResponseSchema
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=GuestsResponseSchema)
def create_guest(guest: GuestsCreateSchema, db: Session = Depends(get_session)):
    logger.info(f"Creating guest with data: {guest.model_dump()}")
    guest_data = guest.model_dump()
    db_guest = Guests(**guest_data)
    db.add(db_guest)
    db.commit()
    db.refresh(db_guest)
    logger.info(f"guest created with ID: {db_guest.id}, and values: {db_guest}")
    return db_guest

@router.get("/{user_id}", response_model=UsersResponseSchema)
def get_user(user_id: int, db: Session = Depends(get_session)):
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
def get_users(db: Session = Depends(get_session)):
    statement = select(Users).where(Users.is_active == True)
    result = db.exec(statement)
    db_users = result.all()
    return db_users


@router.patch("/{user_id}", response_model=UsersResponseSchema)
def update_user(user_id: int, user: UserUpdateSchema, db: Session = Depends(get_session)):
    statement = select(Users).where(Users.id == user_id)
    result = db.exec(statement)
    db_user = result.first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    update_data = user.model_dump(exclude_unset=True)
    db_user.sqlmodel_update(update_data)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_session)):
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
