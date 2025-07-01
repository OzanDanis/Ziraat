# app/persistence/repositories.py

from sqlalchemy.orm import Session
from typing import List
from app.persistence.models import ImportedRecord
from app.persistence.models import (
    ImportedRecord as ImportedRecordModel,
    to_domain,
)
from app.domain.entities import ImportedRecord

class ImportedRecordRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str) -> ImportedRecord:
        """
        Tek bir kayıt ekler.
        """
        record = ImportedRecord(name=name)
        self.db.add(record)
        model = ImportedRecordModel(name=name)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(record)
        return record
        self.db.refresh(model)
        return to_domain(model)

    def bulk_create(self, names: List[str]) -> List[ImportedRecord]:
        """
        Çoklu kayıt ekler.
        """
        objects = [ImportedRecord(name=n) for n in names]
        self.db.bulk_save_objects(objects)
        objects = [ImportedRecordModel(name=n) for n in names]
        self.db.bulk_save_objects(objects, return_defaults=True)
        self.db.commit()
        return objects
        return [to_domain(obj) for obj in objects]

    def list_all(self) -> List[ImportedRecord]:
        """
        Tüm kayıtları döner.
        """
        return self.db.query(ImportedRecord).all()
        records = self.db.query(ImportedRecordModel).all()
        return [to_domain(rec) for rec in records]