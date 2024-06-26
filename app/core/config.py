import os

from dotenv import load_dotenv

os.environ.clear()
load_dotenv()

DEBUG = os.getenv("DEBUG", default=False)

if DEBUG:
    PROJECT_URL = os.getenv("PROJECT_URL", default="http://localhost:8000")
else:
    PROJECT_URL: str = os.getenv("PROJECT_URL")

STATIC_DIRECTORY = os.getcwd() + "/app/static"
TEMPLATES_DIRECTORY = os.getcwd() + "/app/templates"
MEDIA_ADMIN_DIRECTORY = os.getcwd() + "/app/admin/media"
DEBUG = os.getenv("DEBUG", default=True)
DATABASE_URL = os.getenv("DATABASE_URL")
PROJECT_NAME: str = os.getenv("PROJECT_NAME", default="Mis Quince - Selene")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

PROJECT_VERSION: str = "0.0.0"
with open("./version.txt", "r") as file:
    PROJECT_VERSION = file.read().strip()

CORS_ORIGINS: list[str] = ["*"]
