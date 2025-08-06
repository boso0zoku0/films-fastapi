from fastapi import APIRouter

from .films.views import router as views_films_router

router = APIRouter(prefix="/v1")
router.include_router(router=views_films_router)
