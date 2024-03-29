import os

from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv("DEBUG", default=True)
DATABASE_URL = os.getenv("DATABASE_URL")
PROJECT_NAME: str = "Fastapi Template"


PROJECT_VERSION: str = "0.0.0"
with open("./version.txt", "r") as file:
    PROJECT_VERSION = file.read().strip()

CORS_ORIGINS: list[str] = ["*"]

