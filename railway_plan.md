# Railway Deployment Plan

## Goal

Deploy the FastAPI summary-generation app cleanly to Railway.

## Recommended repository structure

```text
lilbro_researcher/
├── app/                    # FastAPI application code
│   ├── main.py
│   ├── generator.py
│   ├── static/
│   └── templates/
├── summaries/              # source markdown summaries
├── generated_outputs/      # generated markdown artifacts
├── README.md
├── requirements.txt
├── Procfile
├── .gitignore
└── railway_plan.md
```

## Why this structure works

- `app/` contains only runtime web application code
- `summaries/` contains curated research inputs
- `generated_outputs/` contains generated artifacts
- top-level deployment files stay simple for Railway

## Deployment concerns

### 1. Ephemeral filesystem
Railway containers do not guarantee durable local storage.

That means:
- `generated_outputs/` is fine for local development
- in production, generated history should eventually move to:
  - Postgres
  - S3 / object storage
  - or another durable store

### 2. Environment variables
Set at least:

- `OPENAI_API_KEY`
- `OPENAI_MODEL` (optional)
- `PORT` (Railway usually injects this)

### 3. Start command
Use the Procfile:

```text
web: uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
```

### 4. Authentication
Current login is intentionally permissive.
Before production, replace it with:
- real password auth
- magic links
- or OAuth

### 5. Persistence roadmap
For Railway-readiness, next refactor should move history storage out of JSON files and into a database-backed service.

## Suggested next refactor

### Phase 1
- Ship current app to Railway as a prototype
- keep summaries in repo
- keep generated outputs ephemeral

### Phase 2
- add database for generation history
- add stored users/auth
- add saved outputs table

### Phase 3
- separate research content from app content if repo grows large
- possibly move summaries to a `data/` service layer or object storage

## Concrete deployment steps

1. Push branch to GitHub
2. Create new Railway project from GitHub repo
3. Set env vars:
   - `OPENAI_API_KEY`
   - optional `OPENAI_MODEL`
4. Confirm Railway detects Python project
5. Deploy using Procfile command
6. Test login, file selection, generation, and download flows

## Recommendation

This repo is now close enough to deploy as a prototype, but for a more serious production version the main structural upgrade should be replacing file-based history/output persistence with a database or object storage layer.
