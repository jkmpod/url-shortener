# main.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from api.endpoints import router
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

# Initialize FastAPI application with detailed documentation
app = FastAPI(
    title="URL Shortener API",
    description="""
    A modern URL shortening service API that allows you to:
    
    * Create shortened URLs
    * Use custom URL codes
    * Retrieve original URLs
    
    ## Features
    
    * **URL Shortening**: Convert long URLs into short, manageable links
    * **Custom URLs**: Create memorable, custom short URLs
    * **Input Validation**: Ensures valid URLs and custom codes
    * **Duplicate Detection**: Prevents URL conflicts
    
    ## Usage
    
    You can use this API directly or through the web interface available at the root URL.
    """,
    version="1.0.0",
    contact={
        "name": "Your Name",
        "url": "https://github.com/yourusername/url-shortener",
        "email": "your.email@example.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    docs_url="/api/docs",  # Custom docs URL
    redoc_url="/api/redoc",  # Custom redoc URL
    openapi_url="/api/openapi.json",  # Custom OpenAPI URL
    debug=settings.DEBUG,
    lifespan=lifespan
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include API routes
app.include_router(
    router,
    prefix=settings.API_PREFIX,
    responses={
        404: {"description": "Not found"},
        400: {"description": "Bad request"},
        500: {"description": "Internal server error"}
    }
)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the URL shortener frontend"""
    return templates.TemplateResponse("index.html", {"request": request})