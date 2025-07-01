import os
import pytest
pytest.importorskip("httpx")
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

# Test ortaminda SQLite kullan
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from app.main import app
from app.infrastructure.db.database import Base, engine, get_db

# Test için ayrı session
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_health():
    resp = client.get("/api/v1/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_upload_preview():
    csv_content = "name,age\nAlice,30\nBob,25\n"
    files = {"file": ("test.csv", csv_content, "text/csv")}
    resp = client.post("/api/v1/upload/preview", files=files)
    assert resp.status_code == 200
    assert resp.json() == ["name", "age"]


def test_upload_commit():
    payload = {
        "columns": ["name", "age"],
        "rows": [["Alice", 30], ["Bob", 25]],
    }
    resp = client.post("/api/v1/upload/commit", json=payload)
    assert resp.status_code == 200
    assert resp.json() == {"inserted": 2}
