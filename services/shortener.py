# app/services/shortener.py
import hashlib
import re
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.models import URL
from app.schemas.url import URLBase

def create_short_url(url: str) -> str:
    """Create a short URL using first 8 characters of MD5 hash"""
    return hashlib.md5(url.encode()).hexdigest()[:8]

def validate_custom_url(custom_url: str) -> bool:
    """
    Validate custom URL:
    - Only alphanumeric characters and hyphens allowed
    - Must be between 4 and 30 characters
    - Cannot start or end with hyphen
    """
    if not custom_url:
        return True
    
    pattern = r'^[a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]$'
    if not re.match(pattern, custom_url):
        return False
    
    if len(custom_url) < 4 or len(custom_url) > 30:
        return False
    
    # Check for reserved words or patterns you don't want to allow
    reserved_words = {'admin', 'api', 'login', 'signup', 'dashboard'}
    if custom_url.lower() in reserved_words:
        return False
    
    return True

def create_url_record(db: Session, url_data: URLBase) -> URL:
    """Create a new URL record"""
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
            raise HTTPException(
                status_code=400,
                detail="Custom URL is already taken"
            )
        
        short_url = url_data.custom_url
        is_custom = True
    else:
        # Generate short URL if no custom URL provided
        short_url = create_short_url(str(url_data.target_url))
        is_custom = False
        
        # Check if URL already exists
        existing_url = db.query(URL).filter(URL.original_url == str(url_data.target_url)).first()
        if existing_url and not existing_url.is_custom:
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
    return db_url

def get_url_by_shortcode(db: Session, short_url: str) -> URL:
    """Retrieve URL record by short code"""
    return db.query(URL).filter(URL.short_url == short_url).first()
