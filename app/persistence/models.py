# app/persistence/models.py

from sqlalchemy import Column, Integer, String
from app.infrastructure.db.database import Base

class ImportedRecord(Base):
    __tablename__ = "imported_records"

    id = Column(Integer, primary_key=True, index=True)
    # String tipine bir maksimum uzunluk giriyoruz (örn. 255),
    # MSSQL’de indexlenebilir bir VARCHAR(255) oluşturur.
    name = Column(String(255), index=True)

# Domain model ile dönüşüm fonksiyonları
from app.domain.entities import ImportedRecord as DomainImportedRecord


def to_domain(model: "ImportedRecord") -> DomainImportedRecord:
    """Persistence modelini domain modeline dönüştürür."""
    return DomainImportedRecord(id=model.id, name=model.name)


def from_domain(entity: DomainImportedRecord) -> "ImportedRecord":
    """Domain modelini persistence modeline dönüştürür."""
    return ImportedRecord(name=entity.name)
