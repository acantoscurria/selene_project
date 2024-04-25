from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi_pagination import add_pagination
from fastapi.templating import Jinja2Templates
from app.api.v1.routers import router as api_v1_router
from dotenv import load_dotenv
from app.core import config
from app.admin.administrator import admin
load_dotenv()

app = FastAPI()

app = FastAPI(
    debug=config.DEBUG,
    title=config.PROJECT_NAME,
    version=config.PROJECT_VERSION,
)

app.mount("/static", StaticFiles(directory=config.STATIC_DIRECTORY), name="static")

templates = Jinja2Templates(directory=config.TEMPLATES_DIRECTORY)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request, name="home.html", context={"config": config}
    )


@app.get("/privacidad", response_class=HTMLResponse)
async def privacidad(request: Request):
    return templates.TemplateResponse(
        request=request, name="privacidad.html", context={"config": config}
    )


add_pagination(app)
app.include_router(api_v1_router, prefix="/api/v1")


if config.CORS_ORIGINS:
    from fastapi.middleware.cors import CORSMiddleware

    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# Mount admin to your app
admin.mount_to(app)
