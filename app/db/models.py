# app/db/models.py
from sqlalchemy import Column, String, DateTime, Boolean
from datetime import datetime
from app.db.base import Base

class URL(Base):
    __tablename__ = "urls"
    
    short_url = Column(String, primary_key=True, index=True)
    original_url = Column(String, index=True)
    is_custom = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
