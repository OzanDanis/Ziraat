# app/presentation/api/v1/routes.py

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import List
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.application.use_cases.upload_data_usecase import UploadDataUseCase
from app.application.use_cases.commit_data_usecase import CommitDataUseCase
from app.infrastructure.db.database import get_db
from app.persistence.repositories import ImportedRecordRepository

router = APIRouter()

@router.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}


@router.post(
    "/upload/preview",
    response_model=List[str],
    summary="Yüklenen dosyanın sütun isimlerini döner"
)
async def upload_preview(file: UploadFile = File(...)):
    """
    Excel veya CSV dosyasını alır, UploadDataUseCase aracılığıyla
    sütun isimlerini okur ve JSON listesi halinde döner.
    """
    use_case = UploadDataUseCase()
    try:
        columns = await use_case.preview_columns(file)
        return columns
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception:
        raise HTTPException(status_code=500, detail="Dosya işlenirken hata oluştu")


class CommitRequest(BaseModel):
    """
    Frontend'den seçili sütun isimleri ve bunlara karşılık gelen
    satır verilerini alır.
    Örnek:
    {
      "columns": ["Name", "Age"],
      "rows": [
        ["Alice", 30],
        ["Bob", 25]
      ]
    }
    """
    columns: List[str]
    rows: List[List]

@router.post(
    "/upload/commit",
    summary="Seçilen sütun ve verileri MSSQL'e kaydeder"
)
async def upload_commit(
    payload: CommitRequest,
    db: Session = Depends(get_db)
):
    repo = ImportedRecordRepository(db)
    use_case = CommitDataUseCase(repo)
    try:
        inserted = use_case.commit(payload.columns, payload.rows)
        return {"inserted": inserted}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception:
        raise HTTPException(status_code=500, detail="Veriler kaydedilirken hata oluştu")
