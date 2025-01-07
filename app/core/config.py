# app/core/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional

class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = "URL Shortener"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database settings
    DATABASE_URL: str = "sqlite:///./shortener.db"
    
    # API settings
    API_PREFIX: str = ""
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE: Optional[str] = "url_shortener.log"
    
    # URL settings
    MIN_CUSTOM_URL_LENGTH: int = 4
    MAX_CUSTOM_URL_LENGTH: int = 30
    AUTO_URL_LENGTH: int = 8
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """Cache and return settings"""
    return Settings()
