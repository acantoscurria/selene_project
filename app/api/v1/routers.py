from fastapi import APIRouter

router = APIRouter()


from .import (
    #agregar aqui mas rutas
    invitees,
    users,
    )


router.include_router(users.router, prefix="/users", tags=["Users"])
router.include_router(invitees.router, prefix="/invitees", tags=["Invitees"])

