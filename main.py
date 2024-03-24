from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, HttpUrl, validator
from typing import Optional
import secrets
from datetime import datetime
from database import Database

app = FastAPI()
db = Database()

class URLItem(BaseModel):
    url: HttpUrl

    @validator('url')
    def validate_url(cls, v):
        if not v.startswith("http://") and not v.startswith("https://"):
            raise ValueError("Invalid URL format. URL must start with 'http://' or 'https://'.")
        return v

@app.post('/create/')
async def create_short_url(url_item: URLItem):
    existing_short_url = db.get_short_url(url_item.url)
    if existing_short_url:
        return {"short_url": f"http://shorter-urls.com/{existing_short_url}"}
    while True:
        short_url = secrets.token_urlsafe(6)
        if not db.short_url_exists(short_url):
            db.save_url(short_url, url_item.url)
            return {"short_url": f"http://shorter-urls.com/{short_url}"}

@app.get('/{short_url}')
async def redirect_to_original(short_url: str, request: Request):
    original_url = db.get_original_url(short_url)
    if original_url:
        country = request.headers.get("X-Forwarded-For", "").split(",")[-1].strip()
        ip_address = request.client.host
        visit_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.save_visit(short_url, country, ip_address, visit_time)
        return HTTPException(status_code=307, detail=original_url)
    else:
        raise HTTPException(status_code=404, detail="Short URL not found")

@app.get('/stats/{short_url}')
async def get_stats(short_url: str):
    visit_count = db.get_stats(short_url)
    return {"short_url": short_url, "visit_count": visit_count}

# Додали опціональні параметри
@app.post('/create_optional_params/')
async def create_short_url_optional_params(url: Optional[str] = None):
    if not url:
        raise HTTPException(status_code=400, detail="URL is required.")
    existing_short_url = db.get_short_url(url)
    if existing_short_url:
        return {"short_url": f"http://shorter-urls.com/{existing_short_url}"}
    while True:
        short_url = secrets.token_urlsafe(6)
        if not db.short_url_exists(short_url):
            db.save_url(short_url, url)
            return {"short_url": f"http://shorter-urls.com/{short_url}"}
