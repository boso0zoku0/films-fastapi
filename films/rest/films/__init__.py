from fastapi import APIRouter

from rest.films.list_views import router as list_views_router

router = APIRouter(prefix="/films")
router.include_router(list_views_router)
