import logging

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api import router as api_router
from api.redirect_views import router as redirect_views_router
from app_lifespan import lifespan
from core.config import settings
from rest import router as rest_router

logging.basicConfig(
    format=settings.logging.log_format,
    level=settings.logging.log_level_name,
    datefmt=settings.logging.date_format,
)
app = FastAPI(lifespan=lifespan)
app.include_router(router=api_router)
app.include_router(router=redirect_views_router)
app.include_router(router=rest_router)
app.mount("/static", StaticFiles(directory="static"), name="static")
