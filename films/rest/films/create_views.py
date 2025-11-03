from fastapi import APIRouter, Request, status
from pydantic import ValidationError
from starlette.responses import HTMLResponse, RedirectResponse

from dependencies.films import GetFilmsStorage
from schemas import FilmsCreate
from services.films import FormHelper
from storage.films.exceptions import FilmsAlreadyExistsError

router = APIRouter(prefix="/create", tags=["Films REST"])

form_helper = FormHelper(model_schema=FilmsCreate, template_name="films/create.html")


@router.get("/", name="films:create-view")
def get_page_create_films(request: Request) -> HTMLResponse:
    return form_helper.render(request)


@router.post("/", name="films:create", response_model=None)
async def create_films(
    request: Request,
    storage: GetFilmsStorage,
) -> RedirectResponse | HTMLResponse:
    async with request.form() as form:
        try:
            film_create = FilmsCreate.model_validate(form)
        except ValidationError as e:
            return form_helper.render(
                request=request,
                pydantic_error=e,
                form_data=form,
                form_validated=True,
            )

    try:
        storage.create_or_raise_if_exists(film_create)
    except FilmsAlreadyExistsError:
        errors = {"slug": f"Film with slug '{film_create.slug}' already exists"}

    else:
        return RedirectResponse(
            url=request.url_for("films:list"),
            status_code=status.HTTP_303_SEE_OTHER,
        )

    return form_helper.render(
        request=request, errors=errors, form_data=film_create, form_validated=True
    )
