import string
import random
from fastapi.testclient import TestClient
from fastapi import status
from schemas.film import FilmsCreate, FilmsRead
from main import app
from tests.test_api.conftest import film


def test_create_film(client: TestClient):
    url = app.url_path_for("create_film")
    data = FilmsCreate(
        name="dwq",
        target_url="https://example.com",
        description="A film",
        year_release=1999,
        slug="".join(
            random.choices(
                string.ascii_letters,
                k=8,
            ),
        ),
    
).model_dump(mode="json")
    response = client.post(url=url, data=data)
    response_data = response.json()
    received_data = {
        "name": data["name"],
        "target_url": data["target_url"],
        "description": data["description"],
        "year_release": data["year_release"],
        "slug": data["slug"],
    }
    assert data == received_data, response_data
    

def test_create_movie_already_exists(film: FilmsRead, auth_client: TestClient) -> None:
    data = FilmsRead(**film.model_dump())
    json = film.model_dump(mode="json")
    url = app.url_path_for("create_film")
    response = auth_client.post(url=url, json=json)
    response_json = response.json()
    assert response.status_code == status.HTTP_409_CONFLICT, response.text
    expected_error = f"Film with slug={film.slug} already exists"
    assert response_json["detail"] == expected_error, response.text