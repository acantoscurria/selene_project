import datetime
from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class UsersSchema(BaseModel):
    email: EmailStr = Field(max_length=255)


    class Config:
        from_attributes = True

class UsersCreateSchema(UsersSchema):
    password: str = Field(max_length=255)
    invite_id: Optional[int] = Field(default=None)

class UserLoginSchema(UsersSchema):
    pass


class UsersResponseSchema(UsersSchema):
    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime


class UserUpdateSchema(BaseModel):
    password: str = Field(max_length=255)






