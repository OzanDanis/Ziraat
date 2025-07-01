from typing import List
from fastapi import UploadFile
from app.infrastructure.file_readers.excel_reader import ExcelReader
from app.infrastructure.file_readers.csv_reader import CSVReader

class UploadDataUseCase:
    """
    Dosya uzantısına göre reader seçer ve sütun listesini döner.
    """
    async def preview_columns(self, file: UploadFile) -> List[str]:
        # Uzantıya bakarak doğru reader'ı seç
        ext = file.filename.split(".")[-1].lower()
        if ext in ("xls", "xlsx"):
            columns = await ExcelReader.get_columns(file)
        elif ext == "csv":
            columns = await CSVReader.get_columns(file)
        else:
            raise ValueError(f"Desteklenmeyen dosya türü: .{ext}")
        return columns