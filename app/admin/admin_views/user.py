# Add view
from typing import Any, Dict
from fastapi import Request
from starlette_admin import BooleanField, DateTimeField, HasOne, StringField, PasswordField
from starlette_admin.contrib.sqla import ModelView

from app.api.v1.authentication import get_password_hash
from app.models.users import Users


class UserView(ModelView):
    identity = "usuarios"
    name = "Usuario"
    label = "Usuarios"
    exclude_fields_from_list = ["password"]
    exclude_fields_from_detail = ["password"]

    fields = [
        StringField("email", "Email", required=True),
        PasswordField("password", "Contraseña", required=True),
        BooleanField("is_active", "Activo",),
        BooleanField("is_admin", "Es Admin"),
        HasOne("invite", "Invitado", identity="invitados"),
    ]

    async def before_create(self, request: Request, data: Dict[str, str], obj: Users) -> None:

        obj.password = get_password_hash(data["password"])

    async def before_edit(self, request: Request, data: Dict[str, Any], obj: Users) -> None:

        if data.get("password", None):
            obj.password = get_password_hash(data["password"])
