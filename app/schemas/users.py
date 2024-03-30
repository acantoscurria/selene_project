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
    invite_id:int = Field(default=None)


class UsersAdminCreateSchema(UsersSchema):
    password : str

class UserLoginSchema(UsersSchema):
    pass


class UsersResponseSchema(UsersSchema):
    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime


class UserUpdateSchema(BaseModel):
    email: Optional[EmailStr] = Field(max_length=255,default=None)
    is_active: Optional[bool] = Field(default=True)
    is_admin: Optional[bool] = Field(default=False)
    password: Optional[str] = Field(max_length=255,default=None)






