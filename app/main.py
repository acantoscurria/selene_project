from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi_pagination import add_pagination
from app.api.v1.routers import router as api_v1_router
from dotenv import load_dotenv
from app.core import config

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
            <p><a class="btn btn-primary" href="/redoc" target="_blank">Ir a Redoc</a></p>
            <p><a class="btn btn-success" href="/docs" target="_blank">Ir a Swagger</a></p>
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

