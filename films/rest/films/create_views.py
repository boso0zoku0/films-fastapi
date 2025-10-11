from fastapi import APIRouter, Form
from typing import Annotated, Any

from fastapi import Request
from starlette.responses import HTMLResponse

from schemas import FilmsCreate
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


@router.post("/", name="films:create")
def create_films(film: Annotated[FilmsCreate, Form()]) -> FilmsCreate:
    return film.model_dump(mode="json")
