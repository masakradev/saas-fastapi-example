# Alembic Migrations

Database migrations management using Alembic.

## Commands

### Create a new migration

Auto-generate migration based on model changes:

```bash
uv run alembic revision --autogenerate -m "description of changes"
```

Create empty migration for manual edits:

```bash
uv run alembic revision -m "description of changes"
```

### Apply migrations

Apply all pending migrations:

```bash
uv run alembic upgrade head
```

Apply next migration only:

```bash
uv run alembic upgrade +1
```

### Rollback migrations

Rollback last migration:

```bash
uv run alembic downgrade -1
```

Rollback all migrations:

```bash
uv run alembic downgrade base
```

### View migration status

Show current revision:

```bash
uv run alembic current
```

Show migration history:

```bash
uv run alembic history
```

## Workflow

1. Modify your SQLModel models
2. Generate migration: `uv run alembic revision --autogenerate -m "add user table"`
3. Edit generated migration in `app/alembic/versions/`
4. Apply migration: `uv run alembic upgrade head`
