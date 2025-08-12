from collections.abc import Generator

import pytest
from _pytest.fixtures import SubRequest
from starlette import status
from starlette.testclient import TestClient

from api.api_v1.film.crud import storage
from schemas.film import FilmsCreate
from tests.test_api.conftest import film_create_random_slug
from main import app
from schemas.film import FilmsCreate, DESCRIPTION_MAX_LENGTH

pytestmark = pytest.mark.apitest


class TestUpdateFilms:

    @pytest.fixture()
    def film(self, request: SubRequest) -> Generator[FilmsCreate]:
        desc, year = request.param
        film = film_create_random_slug(description=desc, year_release=year)
        yield film
        storage.delete(film)

    @pytest.mark.parametrize(
        "film, new_description, new_year_release",
        [
            pytest.param(
                ("old desc", 2010), "new desc", 2012, id="new desc and year release"
            ),
            pytest.param(("qdesc", 2019), "desc", 2011, id="new year release"),
        ],
        indirect=["film"],
    )
    def test_update_movie_details(
        self,
        auth_client: TestClient,
        film: FilmsCreate,
        new_description: str,
        new_year_release: int,
    ) -> None:
        url = app.url_path_for("put_film", slug=film.slug)
        new_film = FilmsCreate(
            name="some-name",
            slug=film.slug,
            description=new_description,
            year_release=new_year_release,
        )
        response = auth_client.put(url=url, json=new_film.model_dump(mode="json"))
        film_db = storage.get_by_slug(film.slug)
        assert response.status_code == status.HTTP_200_OK
        assert film.description != film_db.description
        assert new_film == film_db


class TestFilmsUpdatePartial:

    @pytest.fixture()
    def film(self, request: SubRequest) -> Generator[FilmsCreate]:
        film = film_create_random_slug(description=request.param)
        yield film
        storage.delete(film)

    @pytest.mark.parametrize(
        "film, new_description",
        [
            pytest.param("sdafasfawqesda", "", id="max desc to min desc"),
            pytest.param("", "a" * DESCRIPTION_MAX_LENGTH, id="no desc to max desc"),
        ],
        indirect=["film"],
    )
    def test_film_update_parsial(
        self, new_description: str, auth_client: TestClient, film: FilmsCreate
    ) -> None:
        url = app.url_path_for("patch_film", slug=film.slug)
        response = auth_client.patch(url, json={"description": new_description})
        new_desc_db = storage.get_by_slug(film.slug)
        assert new_description == new_desc_db.description
        assert response.status_code == status.HTTP_200_OK
