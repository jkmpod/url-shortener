# main.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.api.endpoints import router
from app.db.base import engine
from app.db.models import Base
from app.core.config import get_settings
from app.core.logging import setup_logging, get_logger
from contextlib import asynccontextmanager
import os

settings = get_settings()
logger = get_logger(__name__)

# Create templates directory if it doesn't exist
os.makedirs("templates", exist_ok=True)

templates = Jinja2Templates(directory="templates")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle event handler for FastAPI application
    """
    # Setup
    setup_logging()
    logger.info("Starting URL Shortener application")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created")
    
    yield
    
    # Cleanup
    logger.info("Shutting down URL Shortener application")

# Initialize FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include API routes
app.include_router(router, prefix=settings.API_PREFIX)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the URL shortener frontend"""
    return templates.TemplateResponse("index.html", {"request": request})