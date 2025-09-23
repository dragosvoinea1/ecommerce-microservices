import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Setăm variabilele de mediu necesare *înainte* de a importa `app`
os.environ['SECRET_KEY'] = 'test_secret'
os.environ['ALGORITHM'] = 'HS256'

from app.main import app, get_db
from app.db import Base
from app.dependencies import get_current_admin_user

# --- Configurare BD de Test ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_products.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Fixtures ---
@pytest.fixture(scope="function")
def db_session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        return db_session

    def override_get_current_admin_user():
        return {"email": "admin@example.com", "role": "admin"}

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_admin_user] = override_get_current_admin_user
    
    yield TestClient(app)
    app.dependency_overrides.clear()

# --- Teste pentru Categorii ---

def test_create_category(client):
    """Testează crearea cu succes a unei categorii."""
    response = client.post("/categories", json={"name": "Electronice"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Electronice"
    assert "id" in data

def test_get_all_categories(client):
    """Testează preluarea tuturor categoriilor."""
    client.post("/categories", json={"name": "Telefoane"})
    response = client.get("/categories")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Telefoane"

# --- Teste pentru Produse ---

def test_create_product(client, mocker):
    """Testează crearea cu succes a unui produs."""
    # 1. Cream o categorie mai întâi
    category_res = client.post("/categories", json={"name": "Laptopuri"})
    category_id = category_res.json()["id"]

    # 2. Simulăm RabbitMQ
    mock_pika = mocker.patch('pika.BlockingConnection')

    # 3. Creăm produsul
    product_data = {
        "name": "Super Laptop", "description": "Descriere", "price": 4500.0,
        "stock": 15, "image_url": "http://example.com/img.png", "category_id": category_id
    }
    response = client.post("/", json=product_data)

    # 4. Verificăm
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Super Laptop"
    assert data["category"]["id"] == category_id
    mock_pika.return_value.channel.return_value.basic_publish.assert_called_once()


def test_get_all_products(client):
    category_res = client.post(f"/products/categories", json={"name": "Periferice"})
    category_id = category_res.json()["id"]
    product_data = {
        "name": "Mouse Pro", "description": "Descriere", "price": 250.0,
        "stock": 50, "category_id": category_id
    }
    post_response = client.post(f"/products/", json=product_data)
    assert post_response.status_code == 201

    # <<<<<<< CORECTURA ESTE AICI >>>>>>>>>
    # Folosim calea completă pe care o apelează gateway-ul
    response = client.get(f"/products")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Mouse Pro"

def test_delete_product(client, mocker):
    """Testează ștergerea unui produs."""
    # 1. Adăugăm o categorie și un produs
    category_res = client.post("/categories", json={"name": "Audio"})
    category_id = category_res.json()["id"]
    product_data = {"name": "Căști", "price": 300, "stock": 20, "category_id": category_id}
    product_res = client.post("/", json=product_data)
    product_id = product_res.json()["id"]

    # 2. Simulăm RabbitMQ
    mock_pika = mocker.patch('pika.BlockingConnection')
    
    # 3. Ștergem produsul
    response = client.delete(f"/{product_id}")
    assert response.status_code == 204

    # 4. Verificăm că a fost trimis mesajul
    mock_pika.return_value.channel.return_value.basic_publish.assert_called_once()