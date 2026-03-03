# FindKE

A freelance job marketplace platform built with Django and PostgreSQL. Connect clients with freelancers, manage job postings, applications, and complete projects with integrated review and rating systems.

## 🚀 Features

- **User Management**: Client, Freelancer, and Admin roles with JWT authentication
- **Job Management**: Post, apply, and track job projects
- **Job Assignments**: Assign freelancers to jobs with status tracking
- **Reviews & Ratings**: Rate and review completed work
- **Real-time Messaging**: Communicate between clients and freelancers
- **REST API**: Full RESTful API with Django REST Framework
- **JWT Authentication**: Secure token-based authentication with SimpleJWT

## 🛠️ Tech Stack

- **Backend**: Django 5+ with Django REST Framework
- **Database**: PostgreSQL (via Neon)
- **Authentication**: Simple JWT
- **CORS Support**: django-cors-headers
- **Database Driver**: psycopg (PostgreSQL adapter)
- **Environment Management**: python-dotenv

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL database (or Neon account)
- pip or poetry for dependency management

## 🔧 Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/Nebula0999/FindKE.git
cd FindKE
```

### 2. Create and activate virtual environment
```bash
python -m venv .venv

# On Windows
.venv\Scripts\Activate.ps1

# On macOS/Linux
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file in the project root with your Neon PostgreSQL credentials:
```dotenv
PGHOST='your-neon-host.aws.neon.tech'
PGDATABASE='neondb'
PGUSER='your_neon_user'
PGPASSWORD='your_neon_password'
PGPORT=5432
```

Get these credentials from your [Neon Console](https://console.neon.tech) → Project → Connect.

### 5. Run migrations
```bash
python manage.py migrate
```

### 6. Create superuser (optional, for admin panel)
```bash
python manage.py createsuperuser
```

### 7. Start development server
```bash
python manage.py runserver
```

Visit `http://localhost:8000` to verify the connection.

## 📁 Project Structure

```
FindKE/
├── FindKE/              # Main project settings
│   ├── settings.py      # Django configuration with Neon DB settings
│   ├── urls.py          # URL routing
│   ├── views.py         # Test view for DB connection
│   └── wsgi.py
├── users/               # User authentication & profiles
│   ├── models.py        # User, Client, Freelancer, Admin models
│   ├── serializers.py   # DRF serializers
│   ├── views.py         # API endpoints
│   └── migrations/
├── jobs/                # Job posting & management
│   ├── models.py        # JobPosting, JobApplication, JobAssignment, etc.
│   ├── serializers.py   # Job serializers
│   ├── views.py         # Job API endpoints
│   └── migrations/
├── reviews/             # Review & rating system
│   ├── models.py        # Review model
│   └── migrations/
├── core/                # Core utilities
├── templates/           # HTML templates
├── manage.py            # Django management script
├── .env                 # Environment variables (not tracked)
└── README.md            # This file
```

## 🔌 Database Models

### Users
- `User`: Extended Django User with roles (Client, Freelancer, Admin)
- `Client`: Profile for clients with spending and success rates
- `Freelancer`: Profile for freelancers with portfolio and earnings
- `Admin`: Admin profile

### Jobs
- `JobPosting`: Job listings created by clients
- `JobApplication`: Freelancer applications to job postings
- `JobAssignment`: Assignment of freelancer to job
- `JobCompletion`: Job completion tracking and payment
- `Message`: In-app messaging between users

### Reviews
- `Review`: Reviews and ratings after job completion

## 🚀 API Endpoints

### Users
- `GET/POST /users/` - List/create users
- `GET /users/<id>/` - Get user details

### Jobs
- `GET/POST /jobs/` - List/create job postings
- `GET /jobs/<id>/` - Get job details
- `POST /jobs/<id>/apply/` - Apply to a job
- `GET /jobs/<id>/applications/` - Get job applications

### Reviews
- `GET/POST /reviews/` - List/create reviews

## 🧪 Running Tests

```bash
python manage.py test
```

## 📝 Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `PGHOST` | PostgreSQL host | `ep-super-sun.aws.neon.tech` |
| `PGDATABASE` | Database name | `neondb` |
| `PGUSER` | Database user | `neondb_owner` |
| `PGPASSWORD` | Database password | `your-secure-password` |
| `PGPORT` | Database port | `5432` |

## 🐛 Troubleshooting

### Migration Errors
If you encounter migration errors:
```bash
python manage.py migrate --fake-initial
```

### Connection Issues
Verify environment variables are set correctly and Neon instance is active.

### Permission Errors
Make sure you're using the Nebula0999 GitHub account credentials:
```bash
git credential reject https://github.com
```

## 📚 Documentation

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Neon PostgreSQL](https://neon.tech/docs)
- [SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/)

## 👤 Author

**Nebula0999**

## 📄 License

This project is licensed under the MIT License.