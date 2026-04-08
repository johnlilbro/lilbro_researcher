# Railway Deployment Skill

Use this when deploying the `lilbro_researcher` FastAPI app to Railway.

## Goal

Deploy the app as a prototype web service with environment-driven configuration and a clean startup path.

## Preconditions

- Code is pushed to GitHub
- The target branch is ready (for example `devel-railway`)
- Railway account/project access exists
- Required secrets are available

## Required environment variables

- `OPENAI_API_KEY`
- `OPENAI_MODEL` (optional)
- `PORT` is normally injected by Railway

## Required files

- `requirements.txt`
- `Procfile`
- `railway.json`

## Deployment steps

1. Push the branch to GitHub.
2. Create a new Railway project from the GitHub repository.
3. Select the correct branch for deployment.
4. Confirm Railway detects the Python app.
5. Set environment variables in Railway.
6. Deploy and verify the service starts with:
   - `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
7. Open the Railway-generated URL and test:
   - login page
   - summary browsing
   - generation actions
   - download flow

## Important caveats

### Ephemeral filesystem
`generated_outputs/` and `history.json` are currently file-based. On Railway this is acceptable for a prototype, but not durable.

### Authentication
Current auth accepts any username/password. Replace before serious public use.

### Persistence roadmap
For production:
- move history to a database
- move generated artifacts to object storage or DB
- replace permissive auth

## Recommended validation checklist

- app boots successfully
- CSS loads
- summaries appear in the sidebar
- at least one generation action works
- usage panel renders
- download endpoint works
- fallback behavior works if model key is absent

## When to use this skill

Use this guide whenever you need to:
- deploy the current prototype to Railway
- re-deploy after updates
- explain the app's Railway requirements
- audit deployment readiness
