# Railway Persistence Notes

## Current persistence model

The app now uses a hybrid prototype persistence model:

- **SQLite** for generation history and usage metadata
- **Filesystem markdown files** for generated output artifacts

## Why this is okay for now

For a prototype on Railway, this is good enough to validate:
- user flow
- model-backed generation
- usage tracking
- download behavior
- basic operational shape

## Why it is not final

Railway services typically run on ephemeral filesystems unless you introduce managed persistence.

That means:
- SQLite may reset if the service is rebuilt or rescheduled
- generated markdown files may disappear between deploys or container changes

## Transitional deployment stance

Use SQLite on Railway only as a **bridge step**, not a final persistence strategy.

## Best next migration

1. Move generation history to Postgres
2. Move generated markdown outputs to:
   - object storage, or
   - a database table if payload sizes stay manageable
3. Keep `APP_DATA_DIR`, `APP_GENERATED_DIR`, and `APP_DB_PATH` as compatibility knobs during migration

## Benefit of current config approach

Because the app now supports environment-configurable storage paths, future migration will be cleaner and less invasive.
