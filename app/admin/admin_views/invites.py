# Add view
from typing import Any, Dict
from fastapi import Request
from starlette_admin import BooleanField, DateField, DateTimeField, HasOne, IntegerField, StringField
from starlette_admin.contrib.sqla import  ModelView

from app.api.v1.authentication import get_password_hash
from app.models.users import Users



class InviteView(ModelView):
    identity = "invitados"
    name = "Invitado"
    label = "Invitados"

    fields=[
        StringField("name","Nombre",required=True),
        StringField("last_name","Apellido",required=True),
        StringField("gender","Género",),
        DateField("birth_date","Fecha de Nacimiento",output_format="dd-MM-YYYY"),
        StringField("phone_number","Número de teléfono",required=True),
        StringField("address","Dirección",),
        IntegerField("dni","DNI",),
        HasOne("user","Usuario",identity="usuarios"),
    ]
