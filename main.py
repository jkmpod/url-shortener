# main.py
from fastapi import FastAPI
from app.api.endpoints import router
from app.db.base import engine
from app.db.models import Base

app = FastAPI(title="URL Shortener")

# Create database tables
Base.metadata.create_all(bind=engine)

# Include API routes
app.include_router(router)
