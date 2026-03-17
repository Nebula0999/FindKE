"""
Settings package initialization.
Automatically loads the appropriate settings module based on DJANGO_SETTINGS_MODULE.
"""
import os

# Default to development settings if not specified
settings_module = os.getenv('DJANGO_SETTINGS_MODULE', 'FindKE.settings.development')

if 'production' in settings_module:
    from .production import *
elif 'development' in settings_module:
    from .development import *
else:
    from .base import *
