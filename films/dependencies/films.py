from typing import Annotated, cast

from fastapi import Depends, HTTPException, Request
from starlette import status

from core.config import settings
from schemas import FilmsCreate
from storage.films import FilmsStorage


def get_films_storage(request: Request) -> FilmsStorage:
    return request.app.state.films_storage  # type: ignore[no-any-return]


GetFilmsStorage = Annotated[FilmsStorage, Depends(get_films_storage)]


def prefetch_url_film(slug: str, storage: GetFilmsStorage) -> FilmsCreate | None:
    url: FilmsCreate | None = storage.get_by_slug(slug=slug)
    if url:
        return url
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Film {slug!r} not found"
    )


FilmBySlug = Annotated[FilmsCreate, Depends(prefetch_url_film)]
