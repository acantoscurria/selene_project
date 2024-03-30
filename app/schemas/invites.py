from datetime import date
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum


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
    id: int
    name: str = Field(max_length=255)
    last_name: str = Field(max_length=255)
    user: Optional["UsersResponseSchema"]
    photo: Optional[str]

class InvitesUpdateSchema(InvitesSchema):
    name: Optional[str] = Field(max_length=255,default=None)
    last_name: Optional[str] = Field(max_length=255,default=None)
    birth_date: Optional[date] = Field(default=None)
    address: Optional[str] = Field(max_length=255,default=None)
    phone_number: Optional[str] = Field(max_length=255,default=None)


class InvitesUpdatePhoto(BaseModel):
    photo: str = Field(max_length=255)


class InvitesByDniSchema(BaseModel):
    id: int
    dni: int = Field()