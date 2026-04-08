import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.generator import generate

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "app" / "templates"
STATIC_DIR = BASE_DIR / "app" / "static"
SEARCH_DIRS = [BASE_DIR / "summaries", BASE_DIR]
GENERATED_DIR = BASE_DIR / "generated_outputs"
HISTORY_FILE = GENERATED_DIR / "history.json"
GENERATED_DIR.mkdir(exist_ok=True)

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


def slugify(value: str) -> str:
    value = value.lower().replace("/", "-")
    value = re.sub(r"[^a-z0-9._-]+", "-", value)
    return re.sub(r"-+", "-", value).strip("-")


def load_history() -> list[dict]:
    if not HISTORY_FILE.exists():
        return []
    try:
        return json.loads(HISTORY_FILE.read_text())
    except Exception:
        return []


def save_history(history: list[dict]) -> None:
    HISTORY_FILE.write_text(json.dumps(history, indent=2))


def add_history_item(item: dict) -> None:
    history = load_history()
    history.insert(0, item)
    save_history(history[:50])


def session_totals(history: list[dict]) -> dict:
    total_input = sum(int(item.get("usage", {}).get("input_tokens", 0)) for item in history)
    total_output = sum(int(item.get("usage", {}).get("output_tokens", 0)) for item in history)
    total_tokens = sum(int(item.get("usage", {}).get("total_tokens", 0)) for item in history)
    total_cost = sum(float(item.get("usage", {}).get("estimated_cost_usd", 0)) for item in history)
    return {
        "input_tokens": total_input,
        "output_tokens": total_output,
        "total_tokens": total_tokens,
        "estimated_cost_usd": round(total_cost, 6),
    }


def render_app(
    request: Request,
    file: Optional[str] = None,
    generated_output: Optional[str] = None,
    generation_mode: Optional[str] = None,
    usage: Optional[dict] = None,
    saved_file: Optional[str] = None,
):
    files = list_markdown_files()
    selected_file = file if file in files else (files[0] if files else None)
    file_content = read_markdown_file(selected_file) if selected_file else ""
    history = load_history()
    totals = session_totals(history)

    return templates.TemplateResponse(
        "app.html",
        {
            "request": request,
            "title": "lilbro researcher",
            "files": files,
            "selected_file": selected_file,
            "file_content": file_content,
            "generated_output": generated_output,
            "generation_mode": generation_mode,
            "usage": usage,
            "history": history,
            "totals": totals,
            "saved_file": saved_file,
        },
    )


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
def app_home(request: Request, file: Optional[str] = None):
    if not is_logged_in(request):
        return RedirectResponse(url="/", status_code=303)
    return render_app(request, file=file)


@app.post("/generate/{kind}", response_class=HTMLResponse)
def generate_view(request: Request, kind: str, file: str = Form(...)):
    if not is_logged_in(request):
        return RedirectResponse(url="/", status_code=303)

    content = read_markdown_file(file)
    output, generation_mode, usage = generate(kind, file, content)

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")
    generated_name = f"{slugify(kind)}_{timestamp}.md"
    generated_path = GENERATED_DIR / generated_name
    generated_path.write_text(output)

    history_item = {
        "timestamp": timestamp,
        "source_file": file,
        "kind": kind,
        "mode": generation_mode,
        "saved_file": f"generated_outputs/{generated_name}",
        "usage": usage,
    }
    add_history_item(history_item)

    return render_app(
        request,
        file=file,
        generated_output=output,
        generation_mode=generation_mode,
        usage=usage,
        saved_file=f"generated_outputs/{generated_name}",
    )


@app.get("/download")
def download_generated(request: Request, path: str):
    if not is_logged_in(request):
        return RedirectResponse(url="/", status_code=303)
    target = (BASE_DIR / path).resolve()
    if BASE_DIR.resolve() not in target.parents:
        raise ValueError("Invalid path")
    return PlainTextResponse(target.read_text(), media_type="text/markdown")
