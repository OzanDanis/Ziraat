# app/persistence/repositories.py

from sqlalchemy.orm import Session
from typing import List
from app.persistence.models import ImportedRecord

class ImportedRecordRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str) -> ImportedRecord:
        """
        Tek bir kayıt ekler.
        """
        record = ImportedRecord(name=name)
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def bulk_create(self, names: List[str]) -> List[ImportedRecord]:
        """
        Çoklu kayıt ekler.
        """
        objects = [ImportedRecord(name=n) for n in names]
        self.db.bulk_save_objects(objects)
        self.db.commit()
        return objects

    def list_all(self) -> List[ImportedRecord]:
        """
        Tüm kayıtları döner.
        """
        return self.db.query(ImportedRecord).all()
