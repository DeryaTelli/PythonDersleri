from typing import Generator
from fastapi import Header, HTTPException, status
from app.db.session import SessionLocal
from app.core.config import settings


def get_db() -> Generator:
    db = SessionLocal() # yeni bir veritabani oturumu olusturur
    try:
        yield db # oturumu cagiran koda verir ornek olarak repository veya endpoint icinde kullanilmak uzere
    finally:
        db.close()  # is bitince oturum kapatilir

def require_admin_key(x_admin_key: str = Header(..., alias="X-Admin-Key")):  # NEW
    if x_admin_key != settings.ADMIN_API_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid admin key.")
    return True