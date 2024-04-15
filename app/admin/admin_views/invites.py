# Add view
from enum import Enum
from typing import Any, Dict
from fastapi import Request
from starlette_admin import BooleanField, DateField, DateTimeField, EnumField, HasOne, IntegerField, StringField
from starlette_admin.contrib.sqla import  ModelView

from app.api.v1.authentication import get_password_hash
from app.models.invites import Gender
from app.models.users import Users



class InviteView(ModelView):
    identity = "invitados"
    name = "Invitado"
    label = "Invitados"
    exclude_fields_from_create=["user"]

    fields=[
        StringField("name","Nombre",required=True),
        StringField("last_name","Apellido",required=True),
        EnumField("gender","Género",enum=Gender),
        DateField("birth_date","Fecha de Nacimiento",output_format="dd-MM-YYYY"),
        StringField("phone_number","Número de teléfono",required=True),
        StringField("address","Dirección"),
        HasOne("user","Usuario",identity="usuarios"),
    ]
