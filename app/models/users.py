from enum import Enum
from datetime import date
from app.api.v1.authentication import get_password_hash
from bcrypt import gensalt, hashpw
from sqlmodel import Relationship, Field
from typing import Optional
from app.models.global_mixins.timestamp_mixins import TimeStampMixin


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"


class Users(TimeStampMixin, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(max_length=255)
    password: str = Field(max_length=255)
    is_active: bool = Field(default=True)
    is_admin: bool = Field(default=False)
    guest_id: Optional[int] = Field(default=None, foreign_key="guest.id")

    guest: "Guests" = Relationship(back_populates="user")

    def hash_password(self):
        hashed_password = get_password_hash(self.password)
        self.password = hashed_password


class Guests(TimeStampMixin, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=255)
    last_name: str = Field(max_length=255)
    gender: Optional[Gender] = Field()
    birth_date: Optional[date] = Field()
    phone_number: str = Field(max_length=255)
    address: Optional[str] = Field(max_length=255)

    user:  Optional[Users] = Relationship(back_populates="guest")

