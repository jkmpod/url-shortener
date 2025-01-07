# app/services/shortener.py
import hashlib
import re
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.models import URL
from app.schemas.url import URLBase
from ..core.config import get_settings
from ..core.logging import get_logger

settings = get_settings()
logger = get_logger(__name__)


def create_short_url(url: str) -> str:
    """Create a short URL using first N characters of MD5 hash"""
    short_url = hashlib.md5(url.encode()).hexdigest()[:settings.AUTO_URL_LENGTH]
    logger.debug(f"Generated short URL: {short_url} for {url}")
    return short_url

def validate_custom_url(custom_url: str) -> bool:
    """Validate custom URL"""
    if not custom_url:
        return True
    
    pattern = r'^[a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]$'
    if not re.match(pattern, custom_url):
        logger.warning(f"Invalid custom URL format: {custom_url}")
        return False
    
    if len(custom_url) < settings.MIN_CUSTOM_URL_LENGTH or len(custom_url) > settings.MAX_CUSTOM_URL_LENGTH:
        logger.warning(f"Custom URL length out of bounds: {custom_url}")
        return False
    
    # Check for reserved words
    reserved_words = {'admin', 'api', 'login', 'signup', 'dashboard'}
    if custom_url.lower() in reserved_words:
        logger.warning(f"Attempted to use reserved word as custom URL: {custom_url}")
        return False
    
    return True

def create_url_record(db: Session, url_data: URLBase) -> URL:
    """Create a new URL record"""
    try:
        # Handle custom URL if provided
        if url_data.custom_url:
            if not validate_custom_url(url_data.custom_url):
                raise HTTPException(
                    status_code=400, 
                    detail="Invalid custom URL. Use 4-30 alphanumeric characters and hyphens. Cannot start or end with hyphen."
                )
            
            # Check if custom URL is already taken
            existing_url = db.query(URL).filter(URL.short_url == url_data.custom_url).first()
            if existing_url:
                logger.warning(f"Custom URL already taken: {url_data.custom_url}")
                raise HTTPException(
                    status_code=400,
                    detail="Custom URL is already taken"
                )
            
            short_url = url_data.custom_url
            is_custom = True
            logger.info(f"Creating custom URL: {short_url}")
        else:
            # Generate short URL if no custom URL provided
            short_url = create_short_url(str(url_data.target_url))
            is_custom = False
            
            # Check if URL already exists
            existing_url = db.query(URL).filter(URL.original_url == str(url_data.target_url)).first()
            if existing_url and not existing_url.is_custom:
                logger.info(f"Returning existing URL for: {url_data.target_url}")
                return existing_url
        
        # Create new URL entry
        db_url = URL(
            original_url=str(url_data.target_url),
            short_url=short_url,
            is_custom=is_custom
        )
        db.add(db_url)
        db.commit()
        db.refresh(db_url)
        logger.info(f"Created new URL record: {short_url} -> {url_data.target_url}")
        return db_url
        
    except Exception as e:
        logger.error(f"Error creating URL record: {str(e)}")
        raise

def get_url_by_shortcode(db: Session, short_url: str) -> URL:
    """Retrieve URL record by short code"""
    url = db.query(URL).filter(URL.short_url == short_url).first()
    if url:
        logger.debug(f"Retrieved URL for short code: {short_url}")
    else:
        logger.warning(f"No URL found for short code: {short_url}")
    return url
