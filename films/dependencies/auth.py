from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette import status
from starlette.requests import Request

from services.auth import db_redis_users

basic_credentials = HTTPBasic(
    scheme_name="Basic API token",
    description="Your Basic API token from the developer portal",
    auto_error=False,
)
UNSAFE_METHODS = frozenset(
    {
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
    }
)


def validate_basic_auth(credentials: HTTPBasicCredentials | None) -> None:
    if credentials and db_redis_users.validate_user_password(
        username=credentials.username, password=credentials.password
    ):
        return
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={"WWW-Authenticate": "Basic"},
    )


def basic_auth_for_unsafe_methods(
    request: Request,
    credentials: Annotated[
        HTTPBasicCredentials | None, Depends(basic_credentials)
    ] = None,
) -> None:

    if request.method not in UNSAFE_METHODS:
        return

    validate_basic_auth(credentials)
