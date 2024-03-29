import datetime
from datetime import date
from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from app.models.users import User

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"

class Address(BaseModel):
    street_name: str
    street_number: int
    floor: Optional[int] = None
    apartment: Optional[str] = None
    zip_code: int
    neighborhood: str
    city: str
    country: str
    additional_info: Optional[str] = None

class UserCreate(BaseModel):
    cuit: str
    name: str
    email: EmailStr = Field(max_length=255)
    password: str = Field(max_length=255)
    birthdate: date
    gender: Gender
    address: Address

    class Config:
        from_attributes = True

class UserLoginSchema(BaseModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(max_length=255)

class UsersResponseSchema(UserCreate):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

class UserRead(BaseModel):
    cuit: str
    name: str
    birthdate: date
    gender: Gender
    address: Address

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: Optional[str] =None
    birthdate: Optional[date] = None
    gender: Optional[Gender] = None

    class Config:
        from_attributes = True
