from fastapi import APIRouter

router = APIRouter()


from .import (
    #agregar aqui mas rutas
    users
    )


router.include_router(users.router, prefix="/users", tags=["Users"])

