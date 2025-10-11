from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.config import settings
from storage.films import FilmsStorage


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    app.state.films_storage = FilmsStorage(
        name_db=settings.redis.collections_names.films_hash
    )

    yield
