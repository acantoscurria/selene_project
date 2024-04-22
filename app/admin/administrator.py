from fastapi.middleware import Middleware
from starlette_admin import CustomView, DropDown, I18nConfig
from starlette_admin.contrib.sqla import Admin
from app.admin.admin_views.custom_views.upload_users import UploadUsersView
from app.admin.admin_views.invites import InviteView
from app.admin.auth_provider import UsernameAndPasswordProvider
from app.core.config import PROJECT_URL
from app.models.invites import Invites
from app.models.users import Users
from app.core.database import engine
from app.admin.admin_views.user import UserView
import os
from starlette.middleware.sessions import SessionMiddleware
from starlette_admin.views import Link


SECRET_KEY = os.getenv("SECRET_KEY")

# Create admin
admin = Admin(
    engine, 
    title="Selene Admin",
    i18n_config = I18nConfig(default_locale="es"),
    auth_provider=UsernameAndPasswordProvider(),
    middlewares=[Middleware(SessionMiddleware, secret_key=SECRET_KEY)],
    templates_dir='app/admin/templates',
    # logo_url=f"{PROJECT_URL}/static/logo.jpeg",
    # login_logo_url=f"{PROJECT_URL}/static/logo.jpeg"
)

#  Add all of custom views

admin.add_view(
    DropDown(
        "Usuarios",
        icon="fa fa-users",
        views=[
            UserView(Users,icon="fa fa-user"),
            UploadUsersView("Cargar usuarios",icon="fas fa-list",path="/usuarios/upload_users"),
        ],
        always_open=False
    )
)
admin.add_view(InviteView(Invites,icon="fas fa-ticket"))

