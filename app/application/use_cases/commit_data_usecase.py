from typing import List
from app.persistence.repositories import ImportedRecordRepository

class CommitDataUseCase:
    """Verileri dogrular ve veritabanina kaydeder."""

    def __init__(self, repository: ImportedRecordRepository):
        self.repository = repository

    def commit(self, columns: List[str], rows: List[List]) -> int:
        if not columns:
            raise ValueError("Kolon listesi bos olamaz")
        if not rows:
            raise ValueError("Satir verisi bos olamaz")

        # Ornek uygulamada sadece ilk kolonu kaydediyoruz
        names = [row[0] for row in rows]
        created = self.repository.bulk_create(names)
        return len(created)
