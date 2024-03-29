from fastapi import APIRouter

router = APIRouter()


from .import (
    #agregar aqui mas rutas
    invites,
    users,
    )


router.include_router(users.router, prefix="/users", tags=["Users"])
router.include_router(invites.router, prefix="/invites", tags=["Invites"])

