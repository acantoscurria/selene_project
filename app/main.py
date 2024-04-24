from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi_pagination import add_pagination
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


@app.get("/", response_class=HTMLResponse)
async def home():
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{config.PROJECT_NAME}</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous" />
        <link href="{config.PROJECT_URL}/static/styles.css" rel="stylesheet" />
    </head>
    <body>
        <div class="container">
            <h1>{config.PROJECT_NAME}</h1>
            <p class="version">API Versión: {config.PROJECT_VERSION}</p>
            <!--
            <p><a class="btn btn-sm btn-primary" href="/redoc">Ir a Redoc</a></p>
            <p><a class="btn btn-sm btn-success" href="/docs">Ir a Swagger</a></p>
            -->
        </div>
        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.8/dist/umd/popper.min.js" integrity="sha384-I7E8VVD/ismYTF4hNIPjVp/Zjvgyol6VFvRkX/vR+Vc4jQkC+hVqc2pM8ODewa9r" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.min.js" integrity="sha384-0pUGZvbkm6XF6gxjEnlmuGrJXVbNuzT9qBBavbLwCsOGabYfZo0T0to5eqruptLy" crossorigin="anonymous"></script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/privacidad", response_class=HTMLResponse)
async def privacidad():
    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{config.PROJECT_NAME}</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
        <link href="{config.PROJECT_URL}/static/styles.css" rel="stylesheet" />
    </head>
    <body>
        <div class="container">
            <div class="container">
                <h1>Políticas de Privacidad</h1>
                <div class="row mt-3">
                    <div class="col-md-12">
                        <h4 class="resalte">App Móvil</h4>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-12">
                        <p>Si bien, esta política de privacidad está en redacción, te comentamos que esta APP Móvil disponible en el Google PlayStore, necesita permisos para acceder a la Cámara y a tu Galería, para poder compartir fotos y videos del evento.</p>
                        <p>Almacenamos localmente información de tu inicio de sesión. Pero solo guardamos aquellos datos que ingresaste al registrarte. Y también para personalizar otros mensajes dentro de la app.</p>
                        <p>Algo muy importante, no se comparten datos con ningún Socio Comercial.</p>
                        <p>Última Modificación: 24/04/2024.</p>
                    </div>
                </div>
                <div class="row mt-3">
                    <div class="col-md-12">
                        <h4 class="resalte">Sitio Web</h4>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-12">
                        <p>Si bien, esta política de privacidad está en redacción, te comentamos que este Sitio Web no almacena información alguna.</p>
                        <p>Algo muy importante, no se comparten datos con ningún Socio Comercial.</p>
                        <p>Última Modificación: 24/04/2024.</p>
                    </div>
                </div>
            </div>
        </div>
        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.8/dist/umd/popper.min.js" integrity="sha384-I7E8VVD/ismYTF4hNIPjVp/Zjvgyol6VFvRkX/vR+Vc4jQkC+hVqc2pM8ODewa9r" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.min.js" integrity="sha384-0pUGZvbkm6XF6gxjEnlmuGrJXVbNuzT9qBBavbLwCsOGabYfZo0T0to5eqruptLy" crossorigin="anonymous"></script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

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
