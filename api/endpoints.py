# app/api/endpoints.py
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
import validators
from typing import Dict
from app.db.base import get_db
from app.schemas.url import URLBase, URLInfo
from app.services.shortener import create_url_record, get_url_by_shortcode
from app.core.logging import get_logger

# Add tags for API documentation organization
router = APIRouter(tags=["URL Operations"])
logger = get_logger(__name__)

@router.post(
    "/url",
    response_model=URLInfo,
    status_code=status.HTTP_201_CREATED,
    summary="Create a shortened URL",
    response_description="The created short URL details"
)
async def create_url(
    url: URLBase,
    db: Session = Depends(get_db)
) -> URLInfo:
    """
    Create a shortened URL from a target URL.

    Parameters:
    - **target_url**: The original URL to be shortened (must be a valid URL)
    - **custom_url**: Optional custom URL path (4-30 alphanumeric characters and hyphens)

    Returns:
    - **short_url**: The generated or custom short URL code
    - **target_url**: The original URL
    - **is_custom**: Whether this is a custom URL
    - **created_at**: Timestamp of creation

    Example Request:
    ```json
    {
        "target_url": "https://example.com/very/long/url",
        "custom_url": "my-custom-url"  // optional
    }
    ```

    Example Response:
    ```json
    {
        "short_url": "my-custom-url",
        "target_url": "https://example.com/very/long/url",
        "is_custom": true,
        "created_at": "2024-01-07T12:00:00"
    }
    ```

    Raises:
    - **400**: Invalid URL format
    - **400**: Invalid custom URL format
    - **400**: Custom URL already taken
    """
    if not validators.url(str(url.target_url)):
        logger.warning(f"Invalid URL format: {url.target_url}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid URL format"
        )
    
    return create_url_record(db, url)

@router.get(
    "/{short_url}",
    response_model=Dict[str, str],
    summary="Get original URL",
    response_description="The original URL for the given short code",
    responses={
        200: {
            "description": "Original URL found",
            "content": {
                "application/json": {
                    "example": {"url": "https://example.com/very/long/url"}
                }
            }
        },
        404: {
            "description": "URL not found",
            "content": {
                "application/json": {
                    "example": {"detail": "URL not found"}
                }
            }
        }
    }
)
async def redirect_to_url(
    short_url: str,
    db: Session = Depends(get_db)
) -> Dict[str, str]:
    """
    Retrieve the original URL for a given short URL code.

    Parameters:
    - **short_url**: The short URL code to look up (path parameter)

    Returns:
    - **url**: The original URL associated with the short code

    Example:
    - GET /{short_url}
    - Returns: {"url": "https://example.com/original/url"}
    """
    url = get_url_by_shortcode(db, short_url)
    if url is None:
        logger.warning(f"URL not found: {short_url}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="URL not found"
        )
    return {"url": url.original_url}