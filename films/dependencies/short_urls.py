from typing import Annotated

from fastapi import Depends

from core.config import settings
from storage.films import FilmsStorage


def get_films_storage() -> FilmsStorage:
    return FilmsStorage(name_db=settings.redis.collections_names.films_hash)


GetFilmsStorage = Annotated[FilmsStorage, Depends(get_films_storage)]
