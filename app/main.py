from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.generator import generate

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "app" / "templates"
STATIC_DIR = BASE_DIR / "app" / "static"
SEARCH_DIRS = [BASE_DIR / "summaries", BASE_DIR]

app = FastAPI(title="lilbro researcher")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def list_markdown_files() -> list[str]:
    files = []
    for directory in SEARCH_DIRS:
        if directory.exists():
            for path in directory.glob("*.md"):
                rel = path.relative_to(BASE_DIR)
                files.append(str(rel))
    return sorted(set(files))


def read_markdown_file(rel_path: str) -> str:
    target = (BASE_DIR / rel_path).resolve()
    if BASE_DIR.resolve() not in target.parents and target != BASE_DIR.resolve():
        raise ValueError("Invalid path")
    if not target.exists() or target.suffix.lower() != ".md":
        raise FileNotFoundError(rel_path)
    return target.read_text()


def is_logged_in(request: Request) -> bool:
    return request.cookies.get("lilbro_auth") == "1"


@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    if is_logged_in(request):
        return RedirectResponse(url="/app", status_code=303)
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    response = RedirectResponse(url="/app", status_code=303)
    response.set_cookie("lilbro_auth", "1", httponly=True)
    return response


@app.get("/logout")
def logout():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("lilbro_auth")
    return response


@app.get("/app", response_class=HTMLResponse)
def app_home(request: Request, file: Optional[str] = None, generated_output: Optional[str] = None):
    if not is_logged_in(request):
        return RedirectResponse(url="/", status_code=303)

    files = list_markdown_files()
    selected_file = file if file in files else (files[0] if files else None)
    file_content = read_markdown_file(selected_file) if selected_file else ""

    return templates.TemplateResponse(
        "app.html",
        {
            "request": request,
            "title": "lilbro researcher",
            "files": files,
            "selected_file": selected_file,
            "file_content": file_content,
            "generated_output": generated_output,
        },
    )


@app.post("/generate/{kind}", response_class=HTMLResponse)
def generate_view(request: Request, kind: str, file: str = Form(...)):
    if not is_logged_in(request):
        return RedirectResponse(url="/", status_code=303)

    files = list_markdown_files()
    content = read_markdown_file(file)
    output = generate(kind, file, content)

    return templates.TemplateResponse(
        "app.html",
        {
            "request": request,
            "title": "lilbro researcher",
            "files": files,
            "selected_file": file,
            "file_content": content,
            "generated_output": output,
        },
    )
