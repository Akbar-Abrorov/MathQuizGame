from fastapi import APIRouter
from .users.views import router as users_router
from .game import router as games_router
from .shop import router as shops_router

router = APIRouter()

router.include_router(users_router, prefix="/users", tags=["Users"])
router.include_router(games_router, prefix="/games", tags=["Games"])
router.include_router(shops_router, prefix="/shops", tags=["Shops"])