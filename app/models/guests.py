from enum import Enum
from datetime import date
from sqlmodel import Relationship, Field
from typing import Optional
from app.models.global_mixins.timestamp_mixins import TimeStampMixin


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"


class Guests(TimeStampMixin, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=255)
    last_name: str = Field(max_length=255)
    gender: Optional[Gender] = Field()
    birth_date: Optional[date] = Field()
    phone_number: str = Field(max_length=255)
    address: Optional[str] = Field(max_length=255)

    user:  Optional["Users"] = Relationship(back_populates="guest")

