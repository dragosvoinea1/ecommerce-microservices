import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Asigură-te că importurile sunt corecte
from app.main import app, get_db, get_current_user_email
from app.db import Base

# --- Configurare BD de Test ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_wishlist.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Fixture pentru Baza de Date ---
@pytest.fixture(scope="function")
def db_session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Fixture pentru Clientul de Test ---
@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        return db_session

    def override_get_current_user_email():
        return "testuser@example.com"

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user_email] = override_get_current_user_email
    
    yield TestClient(app)
    
    app.dependency_overrides.clear()

# --- Teste ---

def test_add_to_wishlist_success(client):
    """Testează adăugarea cu succes a unui produs."""
    response = client.post("/wishlist", json={"product_id": 101})
    assert response.status_code == 201
    data = response.json()
    assert data["product_id"] == 101
    assert data["user_email"] == "testuser@example.com"

def test_add_duplicate_product_to_wishlist(client):
    """Testează eșecul adăugării unui produs duplicat."""
    client.post("/wishlist", json={"product_id": 101}) # Prima adăugare
    response = client.post("/wishlist", json={"product_id": 101}) # A doua adăugare
    assert response.status_code == 409
    assert response.json()["detail"] == "Produsul este deja în wishlist."

def test_get_wishlist(client):
    """Testează preluarea listei de produse."""
    client.post("/wishlist", json={"product_id": 201})
    client.post("/wishlist", json={"product_id": 202})

    response = client.get("/wishlist")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    product_ids = {item['product_id'] for item in data}
    assert {201, 202} == product_ids

def test_remove_from_wishlist_success(client):
    """Testează ștergerea cu succes a unui produs."""
    client.post("/wishlist", json={"product_id": 301})
    
    delete_res = client.delete("/wishlist/301")
    assert delete_res.status_code == 204

    get_res = client.get("/wishlist")
    assert len(get_res.json()) == 0

def test_remove_nonexistent_item(client):
    """Testează ștergerea unui produs care nu există în listă."""
    response = client.delete("/wishlist/999")
    assert response.status_code == 404