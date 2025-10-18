from collections.abc import Mapping
from typing import Annotated, Any

from fastapi import APIRouter, Form, Request, status
from pydantic import BaseModel, ValidationError
from starlette.responses import HTMLResponse, JSONResponse, RedirectResponse

from dependencies.short_urls import GetFilmsStorage
from schemas import FilmsCreate
from storage.films.exceptions import FilmsAlreadyExistsError
from templating import templates

router = APIRouter(prefix="/create", tags=["Films REST"])


@router.get("/", name="films:create-view")
def get_page_create_films(request: Request) -> HTMLResponse:
    context: dict[str, Any] = {}
    model_schema = FilmsCreate.model_json_schema()
    context.update(model_schema=model_schema)
    return templates.TemplateResponse(
        request=request,
        name="films/create.html",
        context=context,
    )


def parse_pydantic_error(error: ValidationError) -> dict[str, str]:
    return {f"{err['loc'][0]}": err["msg"] for err in error.errors()}


def create_view_validation_response(
    request: Request,
    errors: dict[str, str] | None = None,
    form_data: BaseModel | Mapping[str, Any] | None = None,
    *,
    form_validated: bool = True,
) -> HTMLResponse:
    model_schema = FilmsCreate.model_json_schema()
    context: dict[str, Any] = {}
    context.update(
        errors=errors,
        model_schema=model_schema,
        form_validated=form_validated,
        form_data=form_data,
    )
    return templates.TemplateResponse(
        request=request,
        name="films/create.html",
        context=context,
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


@router.post("/", name="films:create", response_model=None)
async def create_films(
    request: Request,
    storage: GetFilmsStorage,
) -> RedirectResponse | HTMLResponse:
    async with request.form() as form:
        try:
            film_create = FilmsCreate.model_validate(form)
        except ValidationError as e:
            error = parse_pydantic_error(e)
            return create_view_validation_response(
                errors=error, form_data=form, request=request
            )

    try:
        storage.create_or_raise_if_exists(film_create)
    except FilmsAlreadyExistsError:
        errors = {"slug": f"Film with slug '{film_create.slug}' already exists"}

    else:
        return RedirectResponse(
            url=request.url_for("films:list"), status_code=status.HTTP_303_SEE_OTHER
        )

    return create_view_validation_response(
        request=request, errors=errors, form_data=film_create
    )
