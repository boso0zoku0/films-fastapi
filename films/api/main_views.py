from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from templating import templates

router = APIRouter()


@router.get("/home", response_class=HTMLResponse, include_in_schema=False, name="home")
def home_page(
    request: Request,
) -> HTMLResponse:
    context = []
    features = ["Short link generation", "Contact the author", "Paid plan"]
    context.append(features)
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"features": features},
    )


@router.get(
    "/about/", response_class=HTMLResponse, include_in_schema=False, name="about"
)
def about_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="about.html",
    )


@router.get("/")
def read_root(request: Request, name: str = "World") -> dict[str, str]:
    docs_url = request.url.replace(path="/docs", query="")
    return {
        "message": f"Hello {name}",
        "docs": str(docs_url),
    }
