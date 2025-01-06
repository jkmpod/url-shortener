# tests/test_shortener.py
import pytest
from app.services.shortener import create_short_url, validate_custom_url
from app.core.config import get_settings
from app.schemas.url import URLBase

settings = get_settings()

def test_create_short_url():
    """Test auto-generation of short URLs"""
    # Test basic URL shortening
    url = "https://example.com"
    short_url = create_short_url(url)
    assert len(short_url) == settings.AUTO_URL_LENGTH
    assert short_url.isalnum()
    
    # Test consistency
    assert create_short_url(url) == short_url
    
    # Test different URLs generate different codes
    another_url = "https://example.org"
    another_short = create_short_url(another_url)
    assert short_url != another_short

def test_validate_custom_url():
    """Test custom URL validation"""
    # Test valid URLs
    assert validate_custom_url("valid-url")
    assert validate_custom_url("test123")
    assert validate_custom_url("my-custom-url")
    
    # Test invalid URLs
    assert not validate_custom_url("")  # Empty
    assert not validate_custom_url("a" * 31)  # Too long
    assert not validate_custom_url("aa")  # Too short
    assert not validate_custom_url("invalid url")  # Contains space
    assert not validate_custom_url("-invalid")  # Starts with hyphen
    assert not validate_custom_url("invalid-")  # Ends with hyphen
    assert not validate_custom_url("admin")  # Reserved word
    
@pytest.mark.parametrize("url,expected_valid", [
    ("https://example.com", True),
    ("invalid-url", False),
    ("ftp://example.com", False),
])
def test_url_schema_validation(url, expected_valid):
    """Test URL schema validation"""
    try:
        URLBase(target_url=url)
        is_valid = True
    except Exception:
        is_valid = False
    assert is_valid == expected_valid
