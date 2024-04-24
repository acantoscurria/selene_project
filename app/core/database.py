from sqlmodel import create_engine, Session
from sqlalchemy.ext.declarative import declarative_base

from app.core.config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)  # , echo=True)

database = declarative_base()


def get_session():
    with Session(engine) as session:
        yield session
