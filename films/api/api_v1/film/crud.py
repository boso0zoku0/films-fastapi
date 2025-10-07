__all__ = ("storage", "FilmsAlreadyExistsError")

import logging
from collections.abc import Iterable
from typing import cast

from pydantic import BaseModel
from redis import Redis

from core.config import settings
from schemas.film import (
    FilmsCreate,
    FilmsRead,
    FilmsUpdate,
    FilmsUpdatePartial,
)

log = logging.getLogger(__name__)


redis = Redis(
    host=settings.redis.connection.host,
    port=settings.redis.connection.port,
    db=settings.redis.db.films,
    decode_responses=True,
)


class FilmsBaseError(Exception):
    pass


class FilmsAlreadyExistsError(FilmsBaseError):
    pass


class FilmsStorage(BaseModel):
    slug_by_films: dict[str, FilmsRead] = {}
    name_db: str

    def save_films(self, film: FilmsCreate) -> None:
        redis.hset(
            name=self.name_db,
            key=film.slug,
            value=film.model_dump_json(),
        )

    def get(self) -> list[FilmsRead]:
        return [
            FilmsRead.model_validate_json(value)
            for value in cast(
                Iterable[str],
                redis.hvals(
                    name=self.name_db,
                ),
            )
        ]

    def get_by_slug(self, slug: str) -> FilmsCreate | None:
        get_data = cast(
            str | None,
            redis.hget(name=self.name_db, key=slug),
        )
        if get_data:
            return FilmsCreate.model_validate_json(get_data)
        return None

    def create_film(self, create_films: FilmsCreate) -> FilmsCreate:
        add_film = FilmsCreate(**create_films.model_dump())
        self.save_films(add_film)
        log.info("Created film: %s", add_film)
        return add_film

    def exists(self, slug: str) -> bool:
        return cast(
            bool,
            redis.hexists(name=self.name_db, key=slug),
        )

    def create_or_raise_if_exists(self, film: FilmsCreate) -> FilmsCreate:
        if not self.exists(film.slug):
            return storage.create_film(film)
        raise FilmsAlreadyExistsError(film.slug)

    def delete_by_slug(self, slug: str) -> None:
        redis.hdel(self.name_db, slug)
        log.info("Deleted film: %s", slug)

    def delete(self, film_url: FilmsCreate) -> None:
        return self.delete_by_slug(slug=film_url.slug)

    def update(self, film: FilmsCreate, film_update: FilmsUpdate) -> FilmsCreate:
        for k, v in film_update:
            setattr(film, k, v)
        self.save_films(film)
        log.info("Updated film to %s", film)
        return film

    def update_partial(
        self, film: FilmsCreate, film_update_partial: FilmsUpdatePartial
    ) -> FilmsCreate:
        for k, v in film_update_partial.model_dump(exclude_unset=True).items():
            setattr(film, k, v)
        self.save_films(film)
        log.info("Updated film to %s", film)
        return film


storage: FilmsStorage = FilmsStorage(
    name_db=settings.redis.collections_names.films_hash
)
