# app/persistence/models.py

from sqlalchemy import Column, Integer, String
from app.infrastructure.db.database import Base

class ImportedRecord(Base):
    __tablename__ = "imported_records"

    id = Column(Integer, primary_key=True, index=True)
    # String tipine bir maksimum uzunluk giriyoruz (örn. 255),
    # MSSQL’de indexlenebilir bir VARCHAR(255) oluşturur.
    name = Column(String(255), index=True)
