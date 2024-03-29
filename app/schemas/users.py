import datetime
from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from .guests import GuestsResponseSchema

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
    guest: Optional[GuestsResponseSchema]
    created_at: datetime.datetime
    updated_at: datetime.datetime


class UserUpdateSchema(BaseModel):
    password: str = Field(max_length=255)






