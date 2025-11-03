from typing import Annotated, Any, Coroutine

from fastapi import APIRouter, Form, Request, status
from starlette.responses import HTMLResponse, RedirectResponse

from dependencies.films import FilmBySlug
from schemas import FilmsUpdate
from services.films import FormHelper
from storage.films import storage
from templating import templates

router = APIRouter(prefix="/{slug}/update")

form_helper = FormHelper(model_schema=FilmsUpdate, template_name="films/update.html")


@router.get("/", name="films:update-views", response_model=None)
async def update_films_views(
    film: FilmBySlug,
    request: Request,
) -> HTMLResponse:
    form_data = FilmsUpdate(**film.model_dump())
    return form_helper.render(request=request, form_data=form_data, film=film)


@router.post("/", name="films:update", response_model=None)
async def update_films(
    film: FilmBySlug,
    film_update: Annotated[FilmsUpdate, Form()],
    request: Request,
) -> RedirectResponse:
    storage.update(film=film, film_update=film_update)
    return RedirectResponse(
        url=request.url_for("films:list"),
        status_code=status.HTTP_303_SEE_OTHER,
    )
