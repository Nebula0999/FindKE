"""
Development settings for FindKE.
"""

from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

# Use console email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Development database - PostgreSQL if env vars present, else SQLite
USE_POSTGRES = all([
    os.getenv('PGHOST'),
    os.getenv('PGDATABASE'),
    os.getenv('PGUSER'),
    os.getenv('PGPASSWORD'),
])

if USE_POSTGRES:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'HOST': os.getenv('PGHOST'),
            'NAME': os.getenv('PGDATABASE'),
            'USER': os.getenv('PGUSER'),
            'PASSWORD': os.getenv('PGPASSWORD'),
            'PORT': int(os.getenv('PGPORT', 5432)),
            'OPTIONS': {
                'sslmode': os.getenv('PGSSLMODE', 'prefer'),
            },
            'CONN_HEALTH_CHECKS': True,
        }
    }

# Disable template caching in development
for template in TEMPLATES:
    template['OPTIONS']['debug'] = True

# Show detailed error pages
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# CORS - allow all origins in development
CORS_ALLOW_ALL_ORIGINS = True
