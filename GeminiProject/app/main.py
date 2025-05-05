from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import google.generativeai as genai

from app.database.database import Base, engine
from app.routers import auth, code_analysis, users
from config.settings import get_settings

app = FastAPI()

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Veritabanı tabloları
Base.metadata.create_all(bind=engine)

# Ayarlar ve Gemini
settings = get_settings()
genai.configure(api_key=settings.GEMINI_API_KEY)

# API route'ları
app.include_router(auth.router, prefix="/api", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(code_analysis.router, prefix="/api/analysis", tags=["Code Analysis"])


# Frontend dizinini bağlama
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Kök dizin "/" için index.html sunumu
@app.get("/")
async def serve_index():
    return FileResponse("frontend/index.html")