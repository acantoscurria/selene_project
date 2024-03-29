import datetime

from pydantic import Field
from sqlmodel import SQLModel


class TimeStampMixin(SQLModel,table=False):
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)