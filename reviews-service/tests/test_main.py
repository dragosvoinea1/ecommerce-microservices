import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Asigură-te că importurile sunt corecte
from app.main import app, get_db, get_current_user_email
from app.db import Base

# --- 1. Configurare Centralizată ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- 2. Fixture pentru Baza de Date ---
@pytest.fixture(scope="function")
def db_session():
    """
    Creează o bază de date și o sesiune complet noi pentru fiecare test.
    Șterge totul la final.
    """
    # Șterge și recreează tabelele de la zero
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- 3. Fixture pentru Clientul de Test ---
@pytest.fixture(scope="function")
def client(db_session):
    """
    Creează un TestClient nou pentru fiecare test, cu dependența `get_db`
    suprascrisă pentru a folosi sesiunea de test curată.
    """
    def override_get_db():
        return db_session

    def override_get_current_user_email():
        return "testuser@example.com"

    # Aplică suprascrierile
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user_email] = override_get_current_user_email
    
    yield TestClient(app)
    
    # Curăță suprascrierile după test
    app.dependency_overrides.clear()

# --- 4. Teste Refactorizate ---
# Testele nu mai au nevoie de 'db_session' ca argument, ci de 'client'.

def test_create_review_success(client):
    response = client.post(
        "/reviews", json={"product_id": 101, "rating": 5, "comment": "Produs excelent!"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["product_id"] == 101
    assert data["user_email"] == "testuser@example.com"

def test_create_review_invalid_rating(client):
    response = client.post(
        "/reviews", json={"product_id": 102, "rating": 6, "comment": "Rating prea mare"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Rating-ul trebuie să fie între 1 și 5."

def test_get_reviews_for_product(client):
    # Adaugă o recenzie în baza de date curată a acestui test
    client.post("/reviews", json={"product_id": 202, "rating": 4, "comment": "Comentariu de test"})
    
    response = client.get("/reviews/product/202")
    assert response.status_code == 200
    data = response.json()
    
    # Acum aserțiunea va fi mereu corectă
    assert len(data) == 1
    assert data[0]["product_id"] == 202

def test_delete_review_success(client):
    new_review_res = client.post("/reviews", json={"product_id": 303, "rating": 5, "comment": "De șters"})
    new_review_id = new_review_res.json()["id"]

    delete_res = client.delete(f"/reviews/{new_review_id}")
    assert delete_res.status_code == 204

    get_res = client.get("/reviews/product/303")
    assert len(get_res.json()) == 0

def test_delete_review_forbidden(client):
    """
    Testează eșecul ștergerii unei recenzii de către un alt utilizator.
    (Versiune corectată)
    """
    # 1. Creăm o recenzie cu utilizatorul default ("testuser@example.com")
    #    folosind clientul configurat corect de fixture.
    new_review_res = client.post(
        "/reviews",
        json={"product_id": 404, "rating": 3, "comment": "Nu se va șterge"},
    )
    # Adăugăm o verificare pentru a ne asigura că recenzia a fost creată cu succes
    assert new_review_res.status_code == 201, f"Crearea recenziei a eșuat: {new_review_res.text}"
    new_review_id = new_review_res.json()["id"]

    # 2. Suprascriem temporar dependența PENTRU A SIMULA un alt utilizator
    app.dependency_overrides[get_current_user_email] = lambda: "anotheruser@example.com"
    
    # 3. Încercăm să ștergem recenzia cu noul utilizator
    delete_res = client.delete(f"/reviews/{new_review_id}")
    assert delete_res.status_code == 403
    assert delete_res.json()["detail"] == "Nu ai permisiunea să ștergi această recenzie."


def test_delete_nonexistent_review(client):
    response = client.delete("/reviews/99999")
    assert response.status_code == 404