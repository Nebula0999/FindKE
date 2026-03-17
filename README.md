# FindKE API

FindKE is a Django API for user authentication, personal task management, reminders, and GraphQL task queries.

## Stack

- Django 6
- Django REST Framework
- DRF Token Authentication
- Graphene-Django (GraphQL)
- PostgreSQL (Neon) with SQLite fallback for local/CI

## Project Structure

```text
FindKE/
  README.md
  .github/
    workflows/
      ci-cd.yml
  FindKE/
    .env
    manage.py
    requirements.txt
    FindKE/
      settings.py
      urls.py
    users/
    tasks/
    reminders/
```

## Quick Start

1. Create and activate a virtual environment.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

2. Install dependencies.

```powershell
pip install -r .\FindKE\requirements.txt
```

3. Create `.env` at `FindKE/.env`.

```dotenv
SECRET_KEY=your-django-secret-key

# Optional Postgres/Neon settings.
# If missing, app falls back to SQLite automatically.
PGHOST=your-neon-host
PGDATABASE=findke_db
PGUSER=your-neon-user
PGPASSWORD=your-neon-password
PGPORT=5432

# Optional hardening toggle
ENVIRONMENT=production
```

4. Apply migrations.

```powershell
python .\FindKE\manage.py migrate
```

5. Run the API.

```powershell
python .\FindKE\manage.py runserver
```

## Authentication

Protected endpoints use token authentication.

```text
Authorization: Token <your_token>
```

## REST API Endpoints

Base URL:

```text
http://127.0.0.1:8000/api/
```

Users:

- `POST /api/users/register/`
- `POST /api/users/login/`
- `GET /api/users/me/`

Tasks:

- `GET /api/tasks/`
- `POST /api/tasks/`
- `GET /api/tasks/<id>/`
- `PUT/PATCH /api/tasks/<id>/`
- `DELETE /api/tasks/<id>/`

Reminders:

- `GET /api/reminders/`
- `POST /api/reminders/`
- `GET /api/reminders/<id>/`
- `PUT/PATCH /api/reminders/<id>/`
- `DELETE /api/reminders/<id>/`

## GraphQL

GraphQL endpoint:

```text
http://127.0.0.1:8000/graphql/
```

Sample query:

```graphql
query GetMyTasks {
  allTasks {
    id
    ide
    title
    description
    priority
    completed
    createdAt
    updatedAt
  }
}
```

Note: `allTasks` is scoped to the authenticated user.

## CI/CD (GitHub Actions)

Workflow file: `.github/workflows/ci-cd.yml`

CI on pull requests and pushes to `main`:

- install dependencies
- run `manage.py check`
- run migrations
- run tests

CD on push to `main` (after CI passes):

- triggers `DEPLOY_WEBHOOK_URL` if configured in repository secrets

## Notes

- Tasks and reminders are always scoped to the authenticated user.
- Reminder creation/update validates that the selected task belongs to the same user.
- SQLite is used when Postgres environment variables are not provided.
