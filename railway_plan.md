# Railway Deployment Plan

## Goal

Deploy the FastAPI summary-generation app cleanly to Railway.

## Recommended repository structure

```text
lilbro_researcher/
├── app/                    # FastAPI application code
│   ├── main.py
│   ├── generator.py
│   ├── db.py
│   ├── config.py
│   ├── static/
│   └── templates/
├── summaries/              # source markdown summaries
├── generated_outputs/      # generated markdown artifacts (prototype mode)
├── data/                   # sqlite database in local/prototype mode
├── README.md
├── requirements.txt
├── Procfile
├── railway.json
└── railway_plan.md
```

## Why this structure works

- `app/` contains runtime web application code
- `summaries/` contains curated research inputs
- `data/` contains SQLite persistence in prototype mode
- `generated_outputs/` contains generated artifacts for download convenience
- top-level deployment files stay simple for Railway

## Deployment concerns

### 1. Ephemeral filesystem
Railway containers do not guarantee durable local storage.

That means:
- SQLite in `data/app.db` is acceptable for prototype deployment
- `generated_outputs/` is acceptable for prototype deployment
- neither should be treated as durable production persistence

### 2. Environment variables
Set at least:

- `OPENAI_API_KEY`
- `OPENAI_MODEL` (optional)
- `APP_DATA_DIR` (optional)
- `APP_GENERATED_DIR` (optional)
- `APP_DB_PATH` (optional)
- `PORT` (Railway usually injects this)

### 3. Start command
Use the Procfile / Railway config:

```text
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### 4. Authentication
Current login is intentionally permissive.
Before production, replace it with:
- real password auth
- magic links
- or OAuth

### 5. Persistence roadmap
Current persistence model:
- generation history -> SQLite
- generated markdown outputs -> filesystem

Recommended next production upgrade:
- generation history -> Postgres
- generated documents -> object storage or database

## Suggested next refactor

### Phase 1
- Ship current app to Railway as a prototype
- keep summaries in repo
- use SQLite and local generated outputs temporarily

### Phase 2
- add Postgres-backed history and output storage
- add stored users/auth
- migrate file-based generated outputs

### Phase 3
- separate research content from app content if repo grows large
- possibly move summaries to object storage or a content service layer

## Concrete deployment steps

1. Push branch to GitHub
2. Create a new Railway project from the GitHub repo
3. Select branch `devel`
4. Set env vars:
   - `OPENAI_API_KEY`
   - optional `OPENAI_MODEL`
   - optional `APP_DATA_DIR`
   - optional `APP_GENERATED_DIR`
   - optional `APP_DB_PATH`
5. Confirm Railway detects the Python project
6. Deploy using Railway config / Procfile command
7. Test login, file selection, generation, history, usage, and download flows

## Recommendation

This repo is now ready for a **prototype Railway deployment** using SQLite as a transitional persistence layer. The right long-term step is to replace SQLite and filesystem output storage with production-grade managed persistence.
