# main.py
from fastapi import FastAPI
from app.api.endpoints import router
from app.db.base import engine
from app.db.models import Base
from app.core.config import get_settings
from app.core.logging import setup_logging, get_logger
from contextlib import asynccontextmanager

settings = get_settings()
logger = get_logger(__name__)

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

# Include API routes
app.include_router(router, prefix=settings.API_PREFIX)
