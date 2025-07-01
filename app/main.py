# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.presentation.api.v1.routes import router as api_router

# MSSQL tablolarını yaratmak için
from app.infrastructure.db.database import engine, Base as PersistenceBase

app = FastAPI(
    title="Excel Data Importer",
    version="1.0.0",
    description="Excel/CSV yükle, sütun önizle ve veri tabanına aktar."
)

# React frontend'ten gelen istekleri izinli hale getirir
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API rotalarını bağla
app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
def on_startup():
    """
    Uygulama ayağa kalkarken MSSQL'deki tabloları oluşturur.
    """
    PersistenceBase.metadata.create_all(bind=engine)
