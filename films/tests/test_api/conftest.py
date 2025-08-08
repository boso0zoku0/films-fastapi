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
""""

    def create_film(self, create_films: FilmsCreate) -> FilmsRead:
        add_film = FilmsRead(**create_films.model_dump())
        self.save_films(add_film)
        log.info("Created film: %s", add_film)
        return add_film
            name: str
    target_url: AnyHttpUrl
    description: ShortAnnotated_description
    year_release: int
    
"""
def create_film() -> FilmsRead:
    film_in = FilmsRead(
        name="film",
        target_url="http://example.com",
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
    
