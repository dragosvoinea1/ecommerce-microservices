import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app, get_db, get_current_user_email
from app.db import Base

# --- Configurare Bază de Date de Test ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Creăm tabelele în baza de date de test
Base.metadata.create_all(bind=engine)

# --- Suprascrierea Dependințelor ---

def override_get_db():
    """Dependință suprascrisă pentru a folosi baza de date de test."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

def override_get_current_user_email():
    """Dependință suprascrisă pentru a simula un utilizator logat."""
    return "testuser@example.com"

# Aplicăm suprascrierile în aplicația noastră FastAPI
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user_email] = override_get_current_user_email


# Inițializăm clientul de test
client = TestClient(app)

# --- Testele propriu-zise ---

def test_create_review_success():
    """Testează crearea cu succes a unei recenzii."""
    response = client.post(
        "/reviews",
        json={"product_id": 101, "rating": 5, "comment": "Produs excelent!"},
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["product_id"] == 101
    assert data["rating"] == 5
    assert data["comment"] == "Produs excelent!"
    assert data["user_email"] == "testuser@example.com"
    assert "id" in data
    assert "created_at" in data

def test_create_review_invalid_rating():
    """Testează eșecul creării unei recenzii cu un rating invalid."""
    response = client.post(
        "/reviews",
        json={"product_id": 102, "rating": 6, "comment": "Rating prea mare"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Rating-ul trebuie să fie între 1 și 5."}

def test_get_reviews_for_product():
    """Testează preluarea recenziilor pentru un produs."""
    # Mai întâi, adăugăm o recenzie pentru a avea ce să preluăm
    client.post(
        "/reviews",
        json={"product_id": 202, "rating": 4, "comment": "Bun, dar se putea și mai bine."},
    )
    
    response = client.get("/reviews/product/202")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["product_id"] == 202
    assert data[0]["comment"] == "Bun, dar se putea și mai bine."