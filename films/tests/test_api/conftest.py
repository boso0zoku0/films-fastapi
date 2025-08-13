import random
import string
from typing import Generator

import pytest
from fastapi.testclient import TestClient

from api.api_v1.auth.services import db_redis_tokens
from main import app
from schemas.film import FilmsRead, FilmsCreate, Films
from api.api_v1.film.crud import storage


@pytest.fixture()
def client() -> Generator[TestClient]:
    with TestClient(app) as client:
        yield client


@pytest.fixture()
def generate_token() -> Generator[str]:
    token = db_redis_tokens.generate_and_save_token()
    yield token
    db_redis_tokens.delete_token(token)


@pytest.fixture()
def auth_client(generate_token: str) -> Generator[TestClient]:
    headers = {"Authorization": f"Bearer {generate_token}"}
    with TestClient(app=app, headers=headers) as client:
        yield client


def create_film() -> FilmsRead:
    film_in = FilmsRead(
        name="film",
        description="A film",
        year_release=1,
        slug="film",
    )
    return storage.create_film(film_in)


@pytest.fixture()
def film() -> Generator[FilmsRead]:
    film = create_film()
    yield film
    storage.delete(film)


def build_film_create(
    slug: str, description: str = "A short url", year_release: int = 2000
) -> FilmsCreate:
    return FilmsCreate(
        slug=slug, name="qweabc", description=description, year_release=year_release
    )


def create_film_exists(
    slug: str, year_release: int = 2000, description: str = "A short url"
) -> FilmsCreate:
    film = build_film_create(
        slug=slug, description=description, year_release=year_release
    )
    return storage.create_film(film)


def build_film_create_random_slug(
    description: str = "A short url",
    year_release: int = 2000,
) -> FilmsCreate:
    return build_film_create(
        slug="".join(random.choices(string.ascii_letters, k=5)),
        description=description,
        year_release=year_release,
    )


def create_film_random_slug(
    description: str = "A short url", year_release: int = 2000
) -> FilmsCreate:
    short_url = build_film_create_random_slug(
        description=description, year_release=year_release
    )
    return storage.create_or_raise_if_exists(short_url)


# def build_film_create(slug: str, description: str = "A short url", year_release: int = 2000) -> FilmsRead:
#     return FilmsRead(
#         slug=slug,
#         name="dwq",
#         description=description,
#         year_release=year_release,
#     )
#
#
# def build_film_create_random_slug() -> FilmsRead:
#     return build_film_create(slug="".join(random.choices(string.ascii_letters, k=4)))
#
#
# def film_create(slug: str) -> FilmsRead:
#     film = build_film_create(slug)
#     return storage.create_film(film)
#
#
# def film_create_random_slug() -> FilmsRead:
#     film = build_film_create_random_slug()
#     return storage.create_film(film)
