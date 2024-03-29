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

@router.get("/{guest_id}", response_model=GuestsResponseSchema)
def get_user(guest_id: int, db: Session = Depends(get_session)):
    logger.info(f"Getting guest with ID: {guest_id}")
    
    statement = select(Guests).where(
        Guests.id == guest_id,
        Guests.is_active == True,
        )
    result = db.exec(statement)
    db_guest = result.first()
    logger.info(f"Getting guest data: {db_guest}")
    if not db_guest:
        logger.error(f"guest with ID: {guest_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="guest not found"
        )
    return db_guest


@router.get("/", response_model=list[GuestsResponseSchema])
def get_guest(db: Session = Depends(get_session)):
    statement = select(Guests).where(Guests.is_active == True)
    result = db.exec(statement)
    db_guest = result.all()
    return db_guest


@router.patch("/{guest_id}", response_model=GuestsResponseSchema)
def update_guest(guest_id: int, guest: GuestsUpdateSchema, db: Session = Depends(get_session)):
    statement = select(Guests).where(Guests.id == guest_id)
    result = db.exec(statement)
    db_guest = result.first()
    if not db_guest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Guest not found"
        )
    update_data = guest.model_dump(exclude_unset=True)
    db_guest.sqlmodel_update(update_data)
    db.commit()
    db.refresh(db_guest)
    return db_guest


@router.delete("/{guest_id}")
def delete_guest(guest_id: int, db: Session = Depends(get_session)):
    statement = select(Guests).where(Guests.id == guest_id)
    result = db.exec(statement)
    db_guest = result.first()
    if not db_guest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Guest not found"
        )
    db.delete(db_guest)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
