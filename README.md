# lilbro_researcher

A research repo for collecting notes, summaries, idea memos, and now a small web app for transforming summary documents into new outputs.

## Research app

This repo now includes a FastAPI web app with:
- a placeholder login page (any username / password works for now)
- summary file browsing
- summary viewing
- generation actions for:
  - startup thesis
  - research agenda
  - PowerPoint-style deck outline
  - 5 best pitch deck ideas

## Run locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000
```

## Notes

Current auth is intentionally permissive for prototyping.
