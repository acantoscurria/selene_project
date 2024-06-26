from fastapi.middleware import Middleware
from starlette_admin import CustomView, DropDown, I18nConfig
from starlette_admin.contrib.sqla import Admin
from app.admin.admin_views.custom_views.upload_invites import UploadInvitesView
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
    i18n_config=I18nConfig(default_locale="es"),
    auth_provider=UsernameAndPasswordProvider(),
    middlewares=[Middleware(SessionMiddleware, secret_key=SECRET_KEY)],
    templates_dir='app/admin/templates',
    # logo_url=f"{PROJECT_URL}/static/logo.jpeg",
    # login_logo_url=f"{PROJECT_URL}/static/logo.jpeg"
)

#  Add all of custom views

admin.add_view(
    DropDown(
        "Invitados",
        icon="fa fa-users",
        views=[
            InviteView(Invites),
            UploadInvitesView("Cargar invitados", icon="fas fa-list", path="/usuarios/upload_invites"),
        ],
        always_open=True
    )
)
admin.add_view(UserView(Users, icon="fas fa-user"))
