# app/__init__.py
from app.core.config import get_settings
from api.endpoints import router

__version__ = "1.0.0"

# This allows importing commonly used components directly from app
# Example: from app import get_settings, router