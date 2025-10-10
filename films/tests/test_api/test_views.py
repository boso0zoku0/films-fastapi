import pytest
from fastapi import status
from fastapi.testclient import TestClient
from starlette.responses import HTMLResponse

from tests.test_api.conftest import client


def test_main_views(client: TestClient) -> None:
    response = client.get("/")
    assert response.template.name == "base.html"  # type: ignore[attr-defined]
    assert response.status_code == status.HTTP_200_OK
