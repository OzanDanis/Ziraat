# app/infrastructure/db/database.py

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Ortam degiskenlerini .env dosyasindan yukle
load_dotenv()

# Bağlantı dizesi ortam değişkeninden okunur, yoksa varsayılan değeri kullanılır
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mssql+pymssql://sa:O159s456D@localhost:1433/excel_importer",
)

# Engine: pymssql kullanıyorsanız fast_executemany parametresi kaldırıldı
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Her istek için session üretecek factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Tüm modellerin Base sınıfı
Base = declarative_base()

def get_db():
    """
    FastAPI dependency: her istekte yeni bir Session açar,
    istek sonunda kapatır.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
