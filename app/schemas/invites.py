from datetime import date
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum
from .users import UsersResponseSchema


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"

class InvitesSchema(BaseModel):
    name: str = Field(max_length=255)
    last_name: str = Field(max_length=255)
    dni: int = Field()
    gender: Optional[Gender]
    birth_date: Optional[date] = Field(default=None)
    address: Optional[str] = Field(default=None)

class InvitesCreateSchema(InvitesSchema):
    phone_number: str = Field(max_length=255)


class InvitesResponseSchema(InvitesSchema):
    user: Optional["UsersResponseSchema"]
    photo: Optional[str]

class InvitesUpdateSchema(InvitesSchema):
    name: Optional[str] = Field(max_length=255)
    last_name: Optional[str] = Field(max_length=255)
    birth_date: Optional[date] = Field()
    address: Optional[str] = Field(max_length=255)
    phone_number: Optional[str] = Field(max_length=255)


class InvitesUpdatePhoto(BaseModel):
    photo: str = Field(max_length=255)