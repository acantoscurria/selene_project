from enum import Enum
from datetime import date
from app.api.v1.authentication import get_password_hash
from bcrypt import gensalt, hashpw
from sqlmodel import Relationship, Field
from typing import Optional
from app.models.global_mixins.timestamp_mixins import TimeStampMixin
from app.models.invitees import Invitees




class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"


class Users(TimeStampMixin, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(max_length=255)
    password: str = Field(max_length=255)
    is_active: bool = Field(default=True)
    is_admin: bool = Field(default=False)
    invite_id: Optional[int] = Field(default=None, foreign_key="invitees.id")

    invite: "Invitees" = Relationship(back_populates="user")

    def hash_password(self):
        hashed_password = get_password_hash(self.password)
        self.password = hashed_password



