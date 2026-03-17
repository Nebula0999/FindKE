# FindKE - Social Network & Chat Platform

FindKE is a production-ready Django backend for a full-featured social network and chat application with real-time capabilities. It provides both GraphQL (primary) and REST API (fallback) interfaces for seamless integration with React frontends.

## 🚀 Features

### User Authentication & Profiles
- ✅ JWT-based authentication
- ✅ Token-based auth (DRF tokens)
- ✅ User registration, login, logout
- ✅ Password reset functionality
- ✅ Email verification
- ✅ Google OAuth integration (django-allauth)
- ✅ Rich user profiles (avatar, bio, location, website)

### Social Networking
- ✅ Follow/unfollow users
- ✅ Friend requests
- ✅ Post feeds (text, images)
- ✅ Like, comment, and repost functionality
- ✅ Nested comments/replies
- ✅ Real-time notifications
- ✅ User search

### Chat/Messaging
- ✅ 1:1 direct messages
- ✅ Group chats
- ✅ Real-time messaging with WebSockets
- ✅ Typing indicators
- ✅ Message read receipts
- ✅ File/image sharing in chats

### Real-Time Features
- ✅ WebSocket support for live chat
- ✅ Real-time notifications
- ✅ Typing indicators
- ✅ Django Channels integration

### Media Handling
- ✅ Image upload with Pillow
- ✅ AWS S3 support
- ✅ Local storage fallback

## 🛠 Technical Stack

- **Django 5.1.5** (LTS)
- **Django REST Framework 3.15.2** (REST API)
- **Graphene-Django 3.2.2** (GraphQL)
- **Django Channels 4.1.0** (WebSockets)
- **Celery 5.4.0** (Background tasks)
- **Redis 5.2.0** (Caching, Channels, Celery)
- **PostgreSQL** (Primary database)
- **Django Allauth 65.3.0** (Social authentication)
- **Pillow 11.0.0** (Image processing)
- **django-storages 1.14.4** (S3 support)

## 📁 Project Structure

```
FindKE/
├── docker-compose.yml              # Docker orchestration
├── Dockerfile                      # Container configuration
├── .env.example                    # Environment variables template
├── README.md                       # This file
├── FRONTEND_INTEGRATION.md         # React integration guide
└── FindKE/
    ├── manage.py
    ├── requirements.txt
    ├── FindKE/
    │   ├── settings/               # Settings module
    │   │   ├── base.py            # Base settings
    │   │   ├── development.py     # Dev settings
    │   │   └── production.py      # Prod settings
    │   ├── urls.py
    │   ├── wsgi.py
    │   ├── asgi.py                # ASGI config for Channels
    │   └── celery.py              # Celery configuration
    ├── users/                      # User authentication & profiles
    ├── accounts/                   # Enhanced auth (allauth)
    ├── posts/                      # Social posts, likes, comments
    ├── chat/                       # Messaging & WebSockets
    ├── notifications/              # Real-time notifications
    ├── graphql/                    # GraphQL schema
    ├── tasks/                      # Task management (legacy)
    └── reminders/                  # Reminders (legacy)
```

## 🚦 Quick Start

### Option 1: Docker (Recommended)

1. **Clone the repository**
```bash
git clone https://github.com/Nebula0999/FindKE.git
cd FindKE
```

2. **Create environment file**
```bash
cp FindKE/.env.example FindKE/.env
# Edit .env with your settings (SECRET_KEY, database credentials, etc.)
```

3. **Start with Docker Compose**
```bash
docker-compose up -d
```

4. **Create superuser**
```bash
docker-compose exec web python manage.py createsuperuser
```

5. **Access the application**
- API: http://localhost:8000/api/
- GraphQL: http://localhost:8000/graphql/
- Admin: http://localhost:8000/admin/

### Option 2: Local Development

1. **Clone the repository**
```bash
git clone https://github.com/Nebula0999/FindKE.git
cd FindKE/FindKE
```

2. **Create and activate virtual environment**
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your settings
```

5. **Install and start PostgreSQL and Redis**
```bash
# Install PostgreSQL and Redis on your system
# Or use Docker:
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=findke_password -e POSTGRES_USER=findke_user -e POSTGRES_DB=findke_db postgres:16-alpine
docker run -d -p 6379:6379 redis:7-alpine
```

6. **Run migrations**
```bash
python manage.py migrate
```

7. **Create superuser**
```bash
python manage.py createsuperuser
```

8. **Collect static files**
```bash
python manage.py collectstatic --noinput
```

9. **Run the development server**
```bash
# Terminal 1: Django/Daphne server
daphne -b 0.0.0.0 -p 8000 FindKE.asgi:application

# Terminal 2: Celery worker
celery -A FindKE worker --loglevel=info

# Terminal 3: Celery beat (optional, for scheduled tasks)
celery -A FindKE beat --loglevel=info
```

## 🔌 API Endpoints

### REST API

**Base URL:** `http://localhost:8000/api/`

#### Authentication
```
POST   /api/users/register/              # Register new user
POST   /api/users/login/                 # Login
GET    /api/users/me/                    # Get current user
POST   /api/users/token/                 # Get JWT token
POST   /api/users/token/refresh/         # Refresh JWT token
```

#### Users & Social
```
GET    /api/users/profiles/              # List users
GET    /api/users/profiles/{id}/         # User profile
POST   /api/users/profiles/{id}/follow/  # Follow user
POST   /api/users/profiles/{id}/unfollow/ # Unfollow user
GET    /api/users/profiles/{id}/followers/ # Get followers
GET    /api/users/profiles/{id}/following/ # Get following
POST   /api/users/friend-requests/       # Send friend request
POST   /api/users/friend-requests/{id}/accept/ # Accept request
POST   /api/users/friend-requests/{id}/reject/ # Reject request
```

#### Posts
```
GET    /api/posts/posts/                 # List posts
POST   /api/posts/posts/                 # Create post
GET    /api/posts/posts/{id}/            # Get post
PUT    /api/posts/posts/{id}/            # Update post
DELETE /api/posts/posts/{id}/            # Delete post
GET    /api/posts/posts/feed/            # Personalized feed
POST   /api/posts/posts/{id}/like/       # Like post
POST   /api/posts/posts/{id}/unlike/     # Unlike post
POST   /api/posts/posts/{id}/repost/     # Repost
GET    /api/posts/comments/              # List comments
POST   /api/posts/comments/              # Create comment
```

#### Chat
```
GET    /api/chat/conversations/          # List conversations
POST   /api/chat/conversations/create_or_get/ # Create/get conversation
GET    /api/chat/messages/               # List messages
POST   /api/chat/messages/               # Send message
POST   /api/chat/messages/{id}/mark_read/ # Mark as read
```

#### Notifications
```
GET    /api/notifications/               # List notifications
POST   /api/notifications/{id}/mark_read/ # Mark as read
POST   /api/notifications/mark_all_read/ # Mark all as read
GET    /api/notifications/unread_count/  # Get unread count
```

### GraphQL API

**Endpoint:** `http://localhost:8000/graphql/`

See the GraphQL playground for interactive documentation and schema exploration.

### WebSocket Endpoints

**Base URL:** `ws://localhost:8000/ws/`

```
ws://localhost:8000/ws/chat/{conversation_id}/  # Chat WebSocket
ws://localhost:8000/ws/notifications/           # Notifications WebSocket
```

## 🔐 Authentication

The API supports multiple authentication methods:

1. **Token Authentication** (DRF)
   ```
   Authorization: Token <your_token>
   ```

2. **JWT Authentication**
   ```
   Authorization: Bearer <your_jwt_token>
   ```

3. **Session Authentication** (for browsable API)

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run tests for specific app
python manage.py test posts

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## 🚀 Deployment

### Environment Variables

Key environment variables to set in production:

```env
# Required
SECRET_KEY=your-very-secret-key
DJANGO_SETTINGS_MODULE=FindKE.settings.production
ENVIRONMENT=production

# Database
PGHOST=your-db-host
PGDATABASE=findke_db
PGUSER=your-db-user
PGPASSWORD=your-db-password
PGPORT=5432

# Redis
REDIS_HOST=your-redis-host
REDIS_PORT=6379

# CORS
CORS_ALLOWED_ORIGINS=https://your-frontend.com
CSRF_TRUSTED_ORIGINS=https://your-api.com

# Optional: AWS S3
USE_S3=True
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_STORAGE_BUCKET_NAME=your-bucket
```

### Production Deployment

The application is configured for deployment on platforms like:
- Render.com
- Heroku
- AWS (with RDS + ElastiCache)
- DigitalOcean App Platform
- Any platform supporting Docker

## 📊 Database Migrations

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migrations
python manage.py showmigrations
```

## 🔧 Admin Interface

Access the Django admin at `http://localhost:8000/admin/` to manage:
- Users
- Posts, Likes, Comments
- Conversations, Messages
- Notifications
- Tasks and Reminders

## 📱 React Integration

See [FRONTEND_INTEGRATION.md](FRONTEND_INTEGRATION.md) for detailed instructions on integrating with React frontends using:
- Apollo Client (GraphQL)
- Axios (REST API)
- WebSocket setup

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👥 Authors

- **Nebula0999** - Initial work

## 🙏 Acknowledgments

- Django and Django REST Framework teams
- Channels and Celery communities
- All open-source contributors
