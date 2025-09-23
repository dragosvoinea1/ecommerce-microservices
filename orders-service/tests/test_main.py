import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Setăm variabilele de mediu necesare *înainte* de a importa `app`
os.environ['PRODUCTS_SERVICE_URL'] = 'http://test-products-service'
os.environ['SECRET_KEY'] = 'test_secret'
os.environ['ALGORITHM'] = 'HS256'

# --- CORECTURĂ 1: Importurile lipsă ---
from app.main import app, get_db, get_current_user_email
from app.db import Base
from app import models # Am adăugat acest import

# --- Configurare BD de Test ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_orders.db"
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
    
    def override_get_current_user_email_mock():
        return "user@example.com"

    app.dependency_overrides[get_db] = override_get_db
    
    # --- CORECTURĂ 2: Suprascrierea dependenței ---
    # Folosim obiectul funcției, nu un string
    app.dependency_overrides[get_current_user_email] = override_get_current_user_email_mock
    
    yield TestClient(app)
    app.dependency_overrides.clear()

# --- Date Simulate ---
mock_product_1 = {"id": 1, "name": "Laptop", "price": 5000, "stock": 10}
mock_product_2 = {"id": 2, "name": "Mouse", "price": 150, "stock": 0}

# --- Teste ---

def test_create_order_success(client, httpx_mock, mocker):
    httpx_mock.add_response(
        method="GET",
        url=f"{os.environ['PRODUCTS_SERVICE_URL']}/products/{mock_product_1['id']}",
        json=mock_product_1
    )
    mock_pika = mocker.patch('pika.BlockingConnection')

    order_data = {"items": [{"product_id": 1, "quantity": 2}]}
    response = client.post("/orders", json=order_data)

    assert response.status_code == 201, response.text
    data = response.json()
    assert data["owner_email"] == "user@example.com"
    assert data["total_amount"] == mock_product_1["price"] * 2
    mock_pika.return_value.channel.return_value.basic_publish.assert_called_once()

def test_create_order_insufficient_stock(client, httpx_mock):
    httpx_mock.add_response(
        method="GET",
        url=f"{os.environ['PRODUCTS_SERVICE_URL']}/products/{mock_product_2['id']}",
        json=mock_product_2
    )
    order_data = {"items": [{"product_id": 2, "quantity": 1}]}
    response = client.post("/orders", json=order_data)
    assert response.status_code == 400
    assert "Stoc insuficient" in response.json()["detail"]

def test_create_order_product_not_found(client, httpx_mock):
    httpx_mock.add_response(
        method="GET",
        url=f"{os.environ['PRODUCTS_SERVICE_URL']}/products/999",
        status_code=404
    )
    order_data = {"items": [{"product_id": 999, "quantity": 1}]}
    response = client.post("/orders", json=order_data)
    assert response.status_code == 404
    assert "nu a fost găsit" in response.json()["detail"]

def test_get_user_orders(client, db_session):
    # Acum `models` este definit corect
    new_order = models.DBOrder(owner_email="user@example.com", total_amount=100)
    db_session.add(new_order)
    db_session.commit()
    
    response = client.get("/orders")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["owner_email"] == "user@example.com"