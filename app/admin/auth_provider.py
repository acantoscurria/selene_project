
from fastapi import Depends
from sqlmodel import Session, create_engine,select
from starlette.requests import Request
from starlette.responses import Response
from starlette_admin.auth import AdminConfig, AdminUser, AuthProvider
from starlette_admin.exceptions import FormValidationError, LoginFailed
from app.core.config import DATABASE_URL
from app.core.database import engine
from app.api.v1.authentication import verify_password
from app.core.database import get_session
from app.models.users import Users



class UsernameAndPasswordProvider(AuthProvider):

    async def login(
        self,
        username: str,
        password: str,
        remember_me: bool,
        request: Request,
        response: Response,
       
    ) -> Response:
        engine = create_engine(DATABASE_URL, echo=True) #, echo=True)

        with Session(engine) as session:
            statement = select(Users).where(Users.email == username)
            user_db = session.exec(statement).first()

        if not user_db:
            raise LoginFailed("Usuario y/o contraseña incorrectos.")
        

        if not user_db.is_admin:
            raise LoginFailed("No tienes permiso para ingresar a este sitio")

        if verify_password(password, user_db.password):

            request.session.update({
                "username": user_db.email,
                "name": user_db.email,
                "is_admin": user_db.is_admin
                })
            return response

        raise LoginFailed("Invalid username or password")

    async def is_authenticated(self, request) -> bool:
        user = request.session.get("username", None)
        if user:
            """
            Save current `user` object in the request state. Can be used later
            to restrict access to connected user.
            """
            request.state.user = user
            return True

        return False

    def get_admin_config(self, request: Request) -> AdminConfig:
        user = request.state.user  # Retrieve current user
        # Update app title according to current_user
        # custom_app_title = "Hola, " + user + "!"
        custom_app_title = "Selene Admin"
        # Update logo url according to current_user
        return AdminConfig(
            app_title=custom_app_title,
            logo_url=None,
        )

    def get_admin_user(self, request: Request) -> AdminUser:
        user = request.state.user  # Retrieve current user
        photo_url = None
        return AdminUser(username=user, photo_url=photo_url)

    async def logout(self, request: Request, response: Response) -> Response:
        request.session.clear()
        return response