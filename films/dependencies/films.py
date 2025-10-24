from typing import Annotated, cast

from fastapi import Depends, Request

from core.config import settings
from storage.films import FilmsStorage


def get_films_storage(request: Request) -> FilmsStorage:
    return request.app.state.films_storage  # type: ignore[no-any-return]


GetFilmsStorage = Annotated[FilmsStorage, Depends(get_films_storage)]
