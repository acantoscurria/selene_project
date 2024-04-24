import datetime
from datetime import date
from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

from app.schemas.users import UserPostSchema


class PostsSchema(BaseModel):
    title: str
    description: Optional[str] = Field(default=None)
    file_path: Optional[str] = Field(default=None)
    resourse_type: Optional[str] = Field(default=None)


class PostsResponseSchema(PostsSchema):
    user: UserPostSchema
    created_at: datetime.datetime
    updated_at: datetime.datetime


class MediaType(Enum):
    IMAGE = "image"
    VIDEO = "video"


class PostsCreateSchema(BaseModel):
    title: str
    description: Optional[str] = Field(default=None)
    resourse_url: Optional[str] = Field(default=None)


class PostsUpdateSchema(BaseModel):
    post_id: int
    title: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    resourse_url: Optional[str] = Field(default=None)
    likes: Optional[int] = Field(default=0)
