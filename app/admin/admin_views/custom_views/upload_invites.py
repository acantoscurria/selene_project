from datetime import timedelta
from starlette.requests import Request
from starlette.responses import Response
from starlette.templating import Jinja2Templates
from starlette_admin import CustomView
from app.api.v1.authentication import create_access_token
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES


class UploadInvitesView(CustomView):
    async def render(self, request: Request, templates: Jinja2Templates) -> Response:

        access_token_expires = timedelta(minutes=5)

        if request.session.get("is_admin"):
            scope = "admin"
        else:
            scope = "invite"

        access_token = create_access_token(
            data={
                "sub": str(request.session.get("id")),
                "scopes": [scope],
                "is_admin": request.session.get("is_admin"),
            }, expires_delta=access_token_expires
        )

        return templates.TemplateResponse(
            "upload_invites.html",
            context={
                "request": request,
                "token": access_token,
                "upload_invites_active": True
            }
        )
