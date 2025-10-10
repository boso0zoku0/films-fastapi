from typing import Generator

import pytest
from _pytest.fixtures import SubRequest
from starlette import status
from starlette.testclient import TestClient

from main import app
from schemas import FilmsCreate
from schemas.film import DESCRIPTION_MAX_LENGTH
from storage.films.crud import storage
from tests.test_api.conftest import create_film_random_slug


class TestFilmsUpdatePartial:

    @pytest.fixture()
    def film(self, request: SubRequest) -> Generator[FilmsCreate]:
        film = create_film_random_slug(description=request.param)
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
        if new_desc_db:
            assert new_description == new_desc_db.description
            assert response.status_code == status.HTTP_200_OK
