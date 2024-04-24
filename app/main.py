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
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css"
              integrity="sha384-TQsmiRSSTVx8S9k+EcaFbAVP3AqjszGzAbF44akQF8s73sPQ7DZgMVz4M"
              crossorigin="anonymous">
        <style>
            body {{
                padding: 20px;
            }}
            h1 {{
                color: #007BFF;
            }}
            p {{
                margin-bottom: 10px;
            }}
            .version {{
                font-size: 1.2em;
                color: red;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{config.PROJECT_NAME}</h1>
            <p class="version">Versión: {config.PROJECT_VERSION}</p>
            <p><a class="btn btn-primary" href="/redoc">Ir a Redoc</a></p>
            <p><a class="btn btn-success" href="/docs">Ir a Swagger</a></p>
        </div>
        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"
                integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj"
                crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.0.7/dist/umd/popper.min.js"
                integrity="sha384-d3Ae53p8I7zv6YzELRfyg53CUfnvm1CX4fihcPKw1VA7N0Xwoj3PxPTmeIs9LTQe"
                crossorigin="anonymous"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"
                integrity="sha384-B4gt1jrGC7Jh4AgTPSdUtOBvfO8sh+Wy0aAxyBc7pScwx3/jIIciJMrL4dbB4ZH6"
                crossorigin="anonymous"></script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/privacidad", response_class=HTMLResponse)
async def home():
    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{config.PROJECT_NAME}</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css"
              integrity="sha384-TQsmiRSSTVx8S9k+EcaFbAVP3AqjszGzAbF44akQF8s73sPQ7DZgMVz4M"
              crossorigin="anonymous">
        <style>
            body {{
                padding: 20px;
            }}
            h1 {{
                color: #007BFF;
            }}
            p {{
                margin-bottom: 10px;
            }}
            .version {{
                font-size: 1.2em;
                color: red;
            }}
            .resalte {{
                color: #ff4400!important;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Políticas de Privacidad</h1>
            <div class="container">
                <div class="row mt-3">
                    <div class="col-md-12">
                        <h4 class="resalte">App Móvil</h4>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-12">
                        <p class="mb-2">Esta política de privacidad está en redacción, pero te comentamos que esta APP Móvil disponible en el Google PlayStore, no necesita de ningún permiso para funcionar.</p>
                        <p class="mb-2">De todas maneras, almacenamos localmente información de tu inicio de sesión. Pero solo guardamos aquellos datos personales que ingresaste en Perfil de Usuario. La utilizamos para completar la pantalla de Pagar Cuota. Y también para personalizar otros mensajes dentro de la app.</p>
                        <p class="mb-2">Algo muy importante, no compartimos ninguno de estos datos con nuestros Socio Comercial.</p>
                        <p class="mb-2">Última Modificación: 23/04/2024.</p>
                    </div>
                </div>
                <div class="row mt-3">
                    <div class="col-md-12">
                        <h4 class="resalte">Sitio Web</h4>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-12">
                        <p class="mb-2">Esta política de privacidad está en redacción, pero te comentamos que este Sitio Web solo almacena información cuado te registras como Usuario.</p>
                        <p>Algo muy importante, no compartimos ninguno de estos datos con nuestros Socio Comercial.</p>
                        <p class="mb-2">Última Modificación: 23/04/2024.</p>
                    </div>
                </div>
            </div>
        </div>
        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"
                integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj"
                crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.0.7/dist/umd/popper.min.js"
                integrity="sha384-d3Ae53p8I7zv6YzELRfyg53CUfnvm1CX4fihcPKw1VA7N0Xwoj3PxPTmeIs9LTQe"
                crossorigin="anonymous"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"
                integrity="sha384-B4gt1jrGC7Jh4AgTPSdUtOBvfO8sh+Wy0aAxyBc7pScwx3/jIIciJMrL4dbB4ZH6"
                crossorigin="anonymous"></script>
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
