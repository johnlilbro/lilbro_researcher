# Railway Launch Checklist

## 1. Code readiness
- [ ] Latest desired branch is pushed to GitHub
- [ ] `devel` contains the current app code
- [ ] `Procfile` exists
- [ ] `railway.json` exists
- [ ] `requirements.txt` is up to date
- [ ] `README.md` and deployment docs reflect current behavior

## 2. App behavior sanity check locally
- [ ] Run locally with `uvicorn app.main:app --reload`
- [ ] Login page loads
- [ ] Any username / password works
- [ ] Summary list appears
- [ ] Selecting a summary works
- [ ] Startup thesis generation works
- [ ] Research agenda generation works
- [ ] Deck outline generation works
- [ ] 5 pitch deck ideas generation works
- [ ] Usage panel renders
- [ ] Download generated markdown works
- [ ] History appears
- [ ] SQLite file is created in `data/app.db`

## 3. Railway project setup
- [ ] Create a new Railway project
- [ ] Connect the GitHub repo: `johnlilbro/lilbro_researcher`
- [ ] Choose the correct branch to deploy
- [ ] Confirm Railway detects it as a Python app
- [ ] Confirm startup command is:
  - `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## 4. Environment variables
Set these in Railway:

- [ ] `OPENAI_API_KEY`
- [ ] `OPENAI_MODEL` = `gpt-4.1-mini` (or another desired model)
- [ ] `APP_DATA_DIR` = `./data`
- [ ] `APP_GENERATED_DIR` = `./generated_outputs`
- [ ] `APP_DB_PATH` = `./data/app.db`

Notes:
- Railway usually injects `PORT` automatically
- If `OPENAI_API_KEY` is missing, app should still run in template fallback mode

## 5. First deploy verification
After deploy, verify:

- [ ] App boot succeeds
- [ ] No import errors in logs
- [ ] Static CSS loads
- [ ] Login page loads from public Railway URL
- [ ] Login redirects to `/app`
- [ ] Summaries are visible
- [ ] A generation action completes
- [ ] Generated output shows on screen
- [ ] Usage / cost box shows values
- [ ] Download link works
- [ ] No path or permissions errors in logs

## 6. Persistence verification
Because current persistence is prototype-grade:

- [ ] Confirm `data/app.db` is created
- [ ] Confirm a generation is written to SQLite history
- [ ] Confirm a generated markdown file is written
- [ ] Re-open app and verify history still appears during the same deployment lifecycle

## 7. Known prototype caveats
Acknowledge before launch:

- [ ] Auth is intentionally insecure
- [ ] SQLite is not long-term Railway persistence
- [ ] Generated markdown files are on an ephemeral filesystem
- [ ] Re-deploys / restarts may lose persisted local state

## 8. Post-launch next steps
- [ ] Replace placeholder auth
- [ ] Move history from SQLite to Postgres
- [ ] Move generated outputs to object storage or DB
- [ ] Add admin / usage controls
- [ ] Add save/export improvements if needed

## 9. Recommended launch stance
- [ ] Treat first Railway deployment as a prototype / internal demo
- [ ] Do not treat it as production-ready yet
- [ ] Use it to validate workflow and UX before hardening persistence/auth
