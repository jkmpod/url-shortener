# app/schemas/url.py
from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime

class URLBase(BaseModel):
    target_url: HttpUrl
    custom_url: str | None = Field(default=None, min_length=4, max_length=30)

class URLInfo(URLBase):
    short_url: str
    created_at: datetime
    is_custom: bool

    class Config:
        orm_mode = True
