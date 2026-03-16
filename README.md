# FindKE API

FindKE is a Django REST API for user authentication, personal task management, and reminders, backed by Neon PostgreSQL.

## Tech Stack

- Django 6
- Django REST Framework
- DRF Token Authentication
- PostgreSQL (Neon)

## Project Structure

```text
FindKE/
	README.md
	Findke/
		.env
		manage.py
		Findke/
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
pip install django djangorestframework psycopg2-binary python-dotenv
```

3. Create Findke/.env with your Neon credentials.

```dotenv
PGHOST=your-neon-host
PGDATABASE=findke_db
PGUSER=your-neon-user
PGPASSWORD=your-neon-password
PGPORT=5432
SECRET_KEY=your-django-secret-key
```

4. Apply migrations.

```powershell
python .\Findke\manage.py migrate
```

5. Run the API.

```powershell
python .\Findke\manage.py runserver
```

## Authentication

The API uses token authentication.

- Send this header for protected endpoints:

```text
Authorization: Token <your_token>
```

## API Base URL

```text
http://127.0.0.1:8000/api/
```

## Endpoints

### Users

- GET users/register/
	- Returns required input fields and an example payload.
- POST users/register/
	- Registers a user and returns token + user data.
- POST users/login/
	- Returns token + user data for valid credentials.
- GET users/me/
	- Returns authenticated user profile.

### Tasks

- GET tasks/
	- List current user's tasks.
- POST tasks/
	- Create a task for current user.
- GET tasks/<id>/
	- Retrieve one of current user's tasks.
- PUT/PATCH tasks/<id>/
	- Update one of current user's tasks.
- DELETE tasks/<id>/
	- Delete one of current user's tasks.

Task fields:

- ide (UUID, read-only)
- title
- description
- priority (low, medium, high)
- completed
- created_at (read-only)
- updated_at (read-only)

### Reminders

- GET reminders/
	- List current user's reminders.
- POST reminders/
	- Create reminder for one of current user's tasks.
- GET reminders/<id>/
	- Retrieve one of current user's reminders.
- PUT/PATCH reminders/<id>/
	- Update one of current user's reminders.
- DELETE reminders/<id>/
	- Delete one of current user's reminders.

Reminder fields:

- ide (UUID, read-only)
- task (task id)
- title
- description
- remind_at
- created_at (read-only)
- updated_at (read-only)

## Example Flow

1. Register user at POST /api/users/register/.
2. Save token from response.
3. Create tasks at POST /api/tasks/ using Authorization header.
4. Create reminders at POST /api/reminders/ with task id and remind_at.

## Notes

- Tasks and reminders are always scoped to the authenticated user.
- Reminder creation/update validates that the task belongs to the same user.
- Database connection is read from Findke/.env.
