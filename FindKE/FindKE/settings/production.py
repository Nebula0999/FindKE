"""
Production settings for FindKE.
"""

from .base import *
from django.core.exceptions import ImproperlyConfigured

DEBUG = False

# Security settings
if not SECRET_KEY or SECRET_KEY == 'django-insecure-dev-key-change-in-production':
    raise ImproperlyConfigured('SECRET_KEY must be set in production.')

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv('ALLOWED_HOSTS', 'findke.onrender.com').split(',')
    if host.strip()
]

# PostgreSQL is required in production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.getenv('PGHOST'),
        'NAME': os.getenv('PGDATABASE'),
        'USER': os.getenv('PGUSER'),
        'PASSWORD': os.getenv('PGPASSWORD'),
        'PORT': int(os.getenv('PGPORT', 5432)),
        'OPTIONS': {
            'sslmode': 'require',
        },
        'DISABLE_SERVER_SIDE_CURSORS': True,
        'CONN_HEALTH_CHECKS': True,
    }
}

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# CSRF settings
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.getenv('CSRF_TRUSTED_ORIGINS', 'https://findke.onrender.com').split(',')
    if origin.strip()
]

# Email backend for production
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
