# app/api/__init__.py
from fastapi import APIRouter
from .endpoints import router

# Export the router for use in the main application
__all__ = ['router']
