from fastapi import APIRouter

from rest.films.list_views import router as list_views_router
from rest.films.create_views import router as create_views_router

router = APIRouter(prefix="/films")
router.include_router(list_views_router)
router.include_router(create_views_router)
