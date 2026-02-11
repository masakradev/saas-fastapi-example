# SaaS fastapi example

[![python](https://img.shields.io/badge/Python-3.14-3776AB.svg?style=flat&logo=python&logoColor=white
)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.128.8-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

## About

Example SaaS application built with **FastAPI** showcasing modern software architecture patterns:

- 🏗️ **Domain-Driven Design (DDD)** - Clean separation of business logic into bounded contexts
- 📨 **Event-Driven Architecture** - Asynchronous communication between context using domain events
- 🧅 **Clean Architecture** - Layered structure with clear boundaries between domain, application, and infrastructure
- 🔐 **Multi-tenancy** - SaaS-ready with tenant isolation

### Tech Stack

- ⚡ **Fully Async** - Asynchronous from top to bottom using `asyncio`
- 🐘 **PostgreSQL** - Primary database with async support
- 🗄️ **SQLAlchemy 2.0 + SQLModel** - Modern async ORM with Pydantic integration
- 🔄 **Alembic** - Database migrations management
- 👷 **Celery + Redis** - Distributed task queue for background workers

## Installation

### Prerequisites

- Python 3.14+
- [uv](https://docs.astral.sh/uv/) - Fast Python package manager

### Setup

**Install dependencies**:

   ```bash
   uv sync
   ```

   This will create a virtual environment and install all locked dependencies from `uv.lock`.

**Run the application in development mode**:

   ```bash
   fastapi dev app/main.py
   ```

### Adding new dependencies

```bash
uv add <package-name>
```

### Updating dependencies

```bash
uv lock --upgrade
uv sync
```

## Development

### Pre-commit hooks

This project uses [pre-commit](https://pre-commit.com/) to run code quality checks before each commit.

**Install pre-commit hooks**:

```bash
uv run pre-commit install
```

This will automatically run the following checks on `git commit`:
- **black** - Code formatting
- **isort** - Import sorting
- **trailing-whitespace** - Remove trailing whitespace
- **end-of-file-fixer** - Ensure files end with newline
- **check-yaml** - Validate YAML files

**Run manually on all files**:

```bash
uv run pre-commit run --all-files
```
