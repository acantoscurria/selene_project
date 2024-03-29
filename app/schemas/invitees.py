from datetime import date
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum
from .users import UsersResponseSchema


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"

class InviteesSchema(BaseModel):
    name: str = Field(max_length=255)
    last_name: str = Field(max_length=255)
    gender: Optional[Gender] = Field()
    birth_date: Optional[date] = Field()
    address: Optional[str] = Field(max_length=255)

class InviteesCreateSchema(InviteesSchema):
    user_id: int
    phone_number: str = Field(max_length=255)


class InviteesResponseSchema(InviteesSchema):
    user: Optional["UsersResponseSchema"]
    photo: Optional[str]

class InviteesUpdateSchema(InviteesSchema):
    name: Optional[str] = Field(max_length=255)
    last_name: Optional[str] = Field(max_length=255)
    birth_date: Optional[date] = Field()
    address: Optional[str] = Field(max_length=255)
    phone_number: Optional[str] = Field(max_length=255)


class InviteesUpdatePhoto(BaseModel):
    photo: str = Field(max_length=255)