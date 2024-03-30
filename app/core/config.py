import os

from dotenv import load_dotenv

load_dotenv()

STATIC_DIRECTORY = os.getcwd() + "/static"
DEBUG = os.getenv("DEBUG", default=True)
DATABASE_URL = os.getenv("DATABASE_URL")
PROJECT_NAME: str = "Selene Project"
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

PROJECT_VERSION: str = "0.0.0"
with open("./version.txt", "r") as file:
    PROJECT_VERSION = file.read().strip()

CORS_ORIGINS: list[str] = ["*"]

