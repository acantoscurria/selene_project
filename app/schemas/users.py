import datetime
from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

from app.schemas.invites import InvitesResponseSchema

class UsersInviteSchema(BaseModel):
    id: int

class UsersSchema(BaseModel):
    email: EmailStr = Field(max_length=255)


    class Config:
        from_attributes = True

class UsersCreateSchema(UsersSchema):
    password: str = Field(max_length=255)
    phone_number: str = Field()


class UsersAdminCreateSchema(UsersSchema):
    password : str

class UserLoginSchema(UsersSchema):
    pass


class UsersResponseSchema(UsersSchema):
    id: int
    email: EmailStr
    is_active: bool
    is_admin: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    

class UsersResponseCreateSchema(UsersSchema):
    user: UsersResponseSchema
    access_token: str 
    token_type: str


class UserPostSchema(BaseModel):
    email: EmailStr
    invite: InvitesResponseSchema


class UserUpdateSchema(BaseModel):
    email: Optional[EmailStr] = Field(max_length=255,default=None)
    is_active: Optional[bool] = Field(default=True)
    is_admin: Optional[bool] = Field(default=False)
    password: Optional[str] = Field(max_length=255,default=None)

