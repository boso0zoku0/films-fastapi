import logging
import string
import random
from typing import Any

import pytest
from _pytest.fixtures import SubRequest
from fastapi.testclient import TestClient
from fastapi import status
from schemas.film import FilmsCreate, FilmsRead
from main import app
from tests.test_api.conftest import film, build_film_create_random_slug


def test_create_film(caplog: pytest.LogCaptureFixture, auth_client: TestClient):
    caplog.set_level(logging.INFO)
    url = app.url_path_for("create_film")
    film = FilmsCreate(
        name="dwq",
        description="A film",
        year_release=1999,
        slug="".join(
            random.choices(
                string.ascii_letters,
                k=8,
            ),
        ),
    )
    data: dict[str, str] = film.model_dump(mode="json")
    response = auth_client.post(url=url, json=data)
    response_data = response.json()
    received_data = {
        "name": data["name"],
        "description": data["description"],
        "year_release": data["year_release"],
        "slug": data["slug"],
    }
    assert response_data == received_data, response_data
    assert film.slug in caplog.text
    assert "Created film" in caplog.text


def test_create_movie_already_exists(film: FilmsRead, auth_client: TestClient) -> None:
    data = FilmsRead(**film.model_dump())
    json = data.model_dump(mode="json")
    url = app.url_path_for("create_film")
    response = auth_client.post(url=url, json=json)
    response_json = response.json()
    assert response.status_code == status.HTTP_409_CONFLICT, response.text
    expected_error = f"Film with slug={film.slug} already exists"
    assert response_json["detail"] == expected_error, response.text


class TestCreateInvalid:
    @pytest.fixture(
        params=[
            pytest.param(("a", "string_too_short"), id="too-short"),
            pytest.param(("foo-bar-spam-eggs", "string_too_long"), id="too-long"),
        ],
    )
    def film_values(self, request: SubRequest) -> tuple[dict[str, Any], str]:
        build = build_film_create_random_slug()
        build_json = build.model_dump(mode="json")
        slug, error = request.param
        build_json["slug"] = slug
        return build_json, error

    def test_invalid_create_film(
        self, auth_client: TestClient, film_values: tuple[dict[str, Any], str]
    ):
        url = app.url_path_for("create_film")
        data, error = film_values
        response = auth_client.post(url=url, json=data)
        assert (
            response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        ), response.text
        error_detail = response.json()["detail"][0]
        assert error_detail["type"] == error, error_detail
