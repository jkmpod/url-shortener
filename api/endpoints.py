# app/api/endpoints.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import validators
from app.db.base import get_db
from app.schemas.url import URLBase, URLInfo
from app.services.shortener import create_url_record, get_url_by_shortcode

router = APIRouter()

@router.post("/url", response_model=URLInfo)
async def create_url(url: URLBase, db: Session = Depends(get_db)):
    if not validators.url(str(url.target_url)):
        raise HTTPException(status_code=400, detail="Invalid URL format")
    
    return create_url_record(db, url)

@router.get("/{short_url}")
async def redirect_to_url(short_url: str, db: Session = Depends(get_db)):
    db_url = get_url_by_shortcode(db, short_url)
    if db_url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    return {"url": db_url.original_url}
