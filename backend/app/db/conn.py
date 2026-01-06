import psycopg

from fastapi import HTTPException
from app.config import DATABASE_URL

def get_conn():
    if not DATABASE_URL:
        raise HTTPException(status_code=500, detail="DATABASE_URL not set")
    return psycopg.connect(DATABASE_URL)