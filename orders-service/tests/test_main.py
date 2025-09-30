import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import stripe 
from unittest.mock import MagicMock # <-- IMPORT NOU

# Setăm variabilele de mediu necesare *înainte* de a importa `app`
os.environ['PRODUCTS_SERVICE_URL'] = 'http://test-products-service'
os.environ['SECRET_KEY'] = 'test_secret'
os.environ['ALGORITHM'] = 'HS256'
os.environ['STRIPE_SECRET_KEY'] = 'test_stripe_key'

from app.main import app, get_db, get_current_user_email
from app.db import Base
from app import models

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
    app.dependency_overrides[get_current_user_email] = override_get_current_user_email_mock
    
    yield TestClient(app)
    app.dependency_overrides.clear()

# --- Date Simulate ---
mock_product_1 = {"id": 1, "name": "Laptop", "price": 5000, "stock": 10}
mock_product_2 = {"id": 2, "name": "Mouse", "price": 150, "stock": 0}
mock_product_3_discount = {"id": 3, "name": "Tastatura Redusa", "price": 400, "stock": 5, "discount_percentage": 25}

# --- Teste ---
# ... (testele anterioare rămân neschimbate) ...

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

def test_create_order_with_discount(client, httpx_mock, mocker):
    httpx_mock.add_response(
        method="GET",
        url=f"{os.environ['PRODUCTS_SERVICE_URL']}/products/{mock_product_3_discount['id']}",
        json=mock_product_3_discount
    )
    mocker.patch('pika.BlockingConnection')
    order_data = {"items": [{"product_id": 3, "quantity": 2}]}
    price = mock_product_3_discount["price"]
    discount = mock_product_3_discount["discount_percentage"]
    expected_price = price * (1 - discount / 100)
    expected_total = expected_price * 2
    response = client.post("/orders", json=order_data)
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["total_amount"] == expected_total
    assert data["items"][0]["price_at_purchase"] == expected_price

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
    new_order = models.DBOrder(owner_email="user@example.com", total_amount=100)
    db_session.add(new_order)
    db_session.commit()
    response = client.get("/orders")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["owner_email"] == "user@example.com"

# <-- TESTUL PENTRU STRIPE A FOST CORECTAT AICI -->
def test_create_checkout_session_with_discount(client, httpx_mock, mocker):
    """Verifică dacă prețul redus este trimis corect către Stripe."""
    httpx_mock.add_response(
        method="GET",
        url=f"{os.environ['PRODUCTS_SERVICE_URL']}/products/{mock_product_3_discount['id']}",
        json=mock_product_3_discount
    )

    mock_stripe_session = mocker.patch.object(stripe.checkout.Session, 'create')
    
    # --- AICI ESTE CORECTURA ---
    # Creăm un obiect simulat (MagicMock) care are atributul .url
    mock_session_object = MagicMock()
    mock_session_object.url = "http://fake-stripe-url.com"
    mock_stripe_session.return_value = mock_session_object
    # --- SFÂRȘIT CORECTURĂ ---
    
    order_data = {"items": [{"product_id": 3, "quantity": 1}]}
    
    response = client.post("/orders/create-checkout-session", json=order_data)
    
    # Acum acest assert ar trebui să funcționeze
    assert response.status_code == 200
    assert response.json() == {"url": "http://fake-stripe-url.com"}

    price = mock_product_3_discount["price"]
    discount = mock_product_3_discount["discount_percentage"]
    expected_price = price * (1 - discount / 100)
    expected_unit_amount = int(expected_price * 100)

    mock_stripe_session.assert_called_once()
    call_args, call_kwargs = mock_stripe_session.call_args
    assert call_kwargs['line_items'][0]['price_data']['unit_amount'] == expected_unit_amount