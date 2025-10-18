from typing import Any

from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse

from dependencies.short_urls import GetFilmsStorage
from templating import templates

router = APIRouter()


@router.get(
    "/", include_in_schema=False, name="films:list", response_class=HTMLResponse
)
def list_films(request: Request, storage: GetFilmsStorage) -> HTMLResponse:
    context: dict[str, Any] = {}
    films = storage.get()
    context.update(films=films)
    return templates.TemplateResponse(
        request=request,
        name="films/list.html",
        context=context,
    )


# def list_view(
#     request: Request,
#     storage: GetShortUrlsStorage,
# ) -> HTMLResponse:
#     context: dict[str, Any] = {}
#     short_urls = storage.get()
#     context.update(
#         short_urls=short_urls,
#     )
#     return templates.TemplateResponse(
#         request=request,
#         name="short-urls/list.html",
#         context=context,
#     )
