from typing import Annotated

from fastapi import APIRouter, Depends
from starlette.responses import RedirectResponse

from api.api_v1.dependencies import prefetch_url_film
from schemas.film import FilmsRead

router = APIRouter(
    prefix="/r",
    tags=["Redirect"],
)


@router.get("/{slug}")
@router.get("/{slug}/")
def redirect_short_url(
    url: Annotated[
        FilmsRead,
        Depends(prefetch_url_film),
    ],
) -> RedirectResponse:
    return RedirectResponse(
        url=str(url.name),
    )
