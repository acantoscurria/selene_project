from datetime import timedelta
import logging
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlmodel import Session, select
from app.api.v1.authentication import ACCESS_TOKEN_EXPIRE_MINUTES, TokenResponseSchema, create_access_token, is_admin, token_decode, verify_password
from app.models.invites import Invites
from app.models.users import Users
from app.schemas.invites import InvitesResponseSchema, InvitesCreateSchema, InvitesUpdateSchema
from app.core.database import get_session
from fastapi import Body

router = APIRouter()

# Configura el registrador
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=InvitesResponseSchema)
def create_invite(
    invite: InvitesCreateSchema,
    db: Session = Depends(get_session),
    user:int = Depends(token_decode),
    ):
    logger.info(f"Creating invite with data: {invite.model_dump()} {user}")
    if not user.get("is_admin",False):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No autorizado")
    invite_data = invite.model_dump()
    
    if db.exec(select(Invites).where(Invites.dni == invite.dni)).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El invitado ya existe")

    db_invite = Invites(**invite_data)
    db.add(db_invite)
    db.commit()
    db.refresh(db_invite)
    logger.info(f"invite created with ID: {db_invite.id}, and values: {db_invite}")
    return db_invite

@router.get("/{invite_id}", response_model=InvitesResponseSchema)
def get_user(invite_id: int, db: Session = Depends(get_session)):
    logger.info(f"Getting invite with ID: {invite_id}")
    
    statement = select(Invites).where(
        Invites.id == invite_id,
        Invites.is_active == True,
        )
    result = db.exec(statement)
    db_invite = result.first()
    logger.info(f"Getting invite data: {db_invite}")
    if not db_invite:
        logger.error(f"invite with ID: {invite_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="invite not found"
        )
    return db_invite


@router.get("/", response_model=list[InvitesResponseSchema])
def get_invites(db: Session = Depends(get_session)):
    statement = select(Invites)
    result = db.exec(statement)
    db_invites = result.all()
    return db_invites


@router.patch("/{invite_id}", response_model=InvitesResponseSchema)
def update_invite(invite_id: int, invite: InvitesUpdateSchema, db: Session = Depends(get_session)):
    statement = select(Invites).where(Invites.id == invite_id)
    result = db.exec(statement)
    db_invite = result.first()
    if not db_invite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="invite not found"
        )
    update_data = invite.model_dump(exclude_unset=True)
    db_invite.sqlmodel_update(update_data)
    db.commit()
    db.refresh(db_invite)
    return db_invite


@router.delete("/{invite_id}")
def delete_invite(invite_id: int, db: Session = Depends(get_session)):
    statement = select(Invites).where(Invites.id == invite_id)
    result = db.exec(statement)
    db_invite = result.first()
    if not db_invite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="invite not found"
        )
    db.delete(db_invite)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
