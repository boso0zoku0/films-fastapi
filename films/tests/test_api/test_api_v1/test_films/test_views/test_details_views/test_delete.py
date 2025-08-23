from collections.abc import Generator

import pytest
from _pytest.fixtures import SubRequest
from starlette import status
from starlette.testclient import TestClient
from api.api_v1.film.crud import storage
from schemas.film import FilmsRead, FilmsCreate
from main import app

pytestmark = pytest.mark.apitest


def create_film(slug: str) -> FilmsCreate:
    film_in = FilmsCreate(
        name="dwq",
        target_url="https://example.com",
        description="A film",
        year_release=1999,
        slug=slug,
    )
    return storage.create_film(film_in)


@pytest.fixture(
    params=[
        pytest.param("abc", id="min slug"),
        pytest.param("abcqwasw", id="max slug"),
    ]
)
def film(request: SubRequest) -> FilmsCreate:
    return create_film(request.param)


def test_delete_film(film: FilmsCreate, auth_client: TestClient) -> None:
    url = app.url_path_for("delete_film", slug=film.slug)
    response = auth_client.delete(url=url)
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.text
    assert not storage.exists(film.slug)
