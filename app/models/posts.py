from enum import Enum
from datetime import date
from app.api.v1.authentication import get_password_hash
from bcrypt import gensalt, hashpw
from sqlmodel import Relationship, Field
from typing import Optional
from app.models.global_mixins.timestamp_mixins import TimeStampMixin
from app.models.invites import Invites


class Posts(TimeStampMixin, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = Field(default=None)
    file_path: Optional[str] = Field(default=None)
    likes: int = Field(default=0)

    user_id: int = Field(foreign_key="users.id")
    user: "Users" = Relationship(back_populates="posts")
