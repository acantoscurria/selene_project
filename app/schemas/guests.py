from datetime import date
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"

class GuestsSchema(BaseModel):
    name: str = Field(max_length=255)
    last_name: str = Field(max_length=255)
    gender: Optional[Gender] = Field()
    birth_date: Optional[date] = Field()
    address: Optional[str] = Field(max_length=255)

class GuestsCreateSchema(GuestsSchema):
    user_id: int
    phone_number: str = Field(max_length=255)


class GuestsResponseSchema(GuestsSchema):
    user: Optional["UsersResponseSchema"]
    photo: Optional[str]

class GuestsUpdateSchema(GuestsSchema):
    name: Optional[str] = Field(max_length=255)
    last_name: Optional[str] = Field(max_length=255)
    birth_date: Optional[date] = Field()
    address: Optional[str] = Field(max_length=255)
    phone_number: Optional[str] = Field(max_length=255)


class GuestsUpdatePhoto(BaseModel):
    photo: str = Field(max_length=255)