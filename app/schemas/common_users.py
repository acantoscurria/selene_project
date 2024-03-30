import datetime
from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

from app.schemas.invites import InvitesResponseSchema


class CommonUserResponseSchema(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    invite: Optional[InvitesResponseSchema] = None
    created_at: datetime.datetime
    updated_at: datetime.datetime




