from fastapi import APIRouter

router = APIRouter()


from .import (
    #agregar aqui mas rutas
    common_users,
    invites,
    users,
    )


router.include_router(users.router, prefix="/users", tags=["Users"])
router.include_router(invites.router, prefix="/invites", tags=["Invites"])
router.include_router(common_users.router, prefix="/common_users", tags=["Common Users"])

