# app/core/logging.py
import logging
import sys
from typing import List
from app.core.config import get_settings

settings = get_settings()

def setup_logging() -> None:
    """Configure logging for the application"""
    # Create logger
    logger = logging.getLogger("url_shortener")
    logger.setLevel(getattr(logging, settings.LOG_LEVEL))

    # Create formatters and handlers
    handlers: List[logging.Handler] = []
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(settings.LOG_FORMAT))
    handlers.append(console_handler)
    
    # File handler if LOG_FILE is specified
    if settings.LOG_FILE:
        file_handler = logging.FileHandler(settings.LOG_FILE)
        file_handler.setFormatter(logging.Formatter(settings.LOG_FORMAT))
        handlers.append(file_handler)
    
    # Add handlers to logger
    logger.handlers = handlers

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance"""
    return logging.getLogger(f"url_shortener.{name}")
