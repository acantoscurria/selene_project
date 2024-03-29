import datetime
from datetime import date
from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"

class UsersSchema(BaseModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(max_length=255)


    class Config:
        from_attributes = True

class UsersCreateSchema(UsersSchema):
    pass

class UserLoginSchema(UsersSchema):
    pass


class UsersResponseSchema(UsersSchema):
    id: int
    email: EmailStr
    is_active: bool
    guest: Optional["GuestsSchema"]
    created_at: datetime.datetime
    updated_at: datetime.datetime


class UserUpdateSchema(BaseModel):
    password: str = Field(max_length=255)


class UserUpdatePhoto(BaseModel):
    photo: str = Field(max_length=255)



class GuestsSchema(BaseModel):
    name: str = Field(max_length=255)
    last_name: str = Field(max_length=255)
    gender: Optional[Gender] = Field()
    birth_date: Optional[date] = Field()
    phone_number: str = Field(max_length=255)
    address: Optional[str] = Field(max_length=255)

