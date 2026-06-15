# app/__init__.py
from app.core.config import get_settings
from app.api.endpoints import router
from app.db.base import get_db

__version__ = "1.0.0"

__all__ = [
    'get_settings',
    'router',
    'get_db',
    '__version__'
]
