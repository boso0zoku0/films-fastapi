import os

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from templating import templates

router = APIRouter(include_in_schema=False)


@router.get("/home", response_class=HTMLResponse, name="home")
def home_page(request: Request) -> HTMLResponse:
    context = []
    features = ["Short link generation", "Contact the author", "Paid plan"]
    context.append(features)
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"features": features},
    )


@router.get("/about/", response_class=HTMLResponse, name="about")
def about_page(request: Request) -> HTMLResponse:
    context: dict[str, str] = {}
    get_audio_welcome = os.path.join(os.getcwd(), "welcomeSite.mp3")
    context.update(get_audio_welcome=get_audio_welcome)
    return templates.TemplateResponse(
        request=request,
        name="about.html",
        context=context,
    )


@router.get("/", name="root")
def read_root(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="base.html",
    )
