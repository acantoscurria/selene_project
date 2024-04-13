from enum import Enum
from datetime import date

from fastapi import Request
from app.api.v1.authentication import get_password_hash
from bcrypt import gensalt, hashpw
from sqlmodel import Relationship, Field
from typing import Optional
from app.models.global_mixins.timestamp_mixins import TimeStampMixin
from app.models.invites import Invites




class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"


class Users(TimeStampMixin, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(max_length=255,unique=True)
    password: str = Field(max_length=255)
    is_active: bool = Field(default=True)
    is_admin: bool = Field(default=False)

    invite_id: Optional[int] = Field(default=None, foreign_key="invites.id")
    invite: Optional["Invites"] = Relationship(back_populates="user")

    posts: Optional[list["Posts"]] = Relationship(back_populates="user")

    def hash_password(self):
        hashed_password = get_password_hash(self.password)
        self.password = hashed_password

    async def __admin_repr__(self, request: Request):
        return f"{self.email}"
    
    async def __admin_select2_repr__(self, request: Request) -> str:
        return f'<div><span>{self.email}</span></div>'


