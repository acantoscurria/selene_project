from fastapi import APIRouter

router = APIRouter()


from .import (
    #agregar aqui mas rutas
    guests,
    users,
    )


router.include_router(users.router, prefix="/users", tags=["Users"])
router.include_router(guests.router, prefix="/guests", tags=["Guests"])

