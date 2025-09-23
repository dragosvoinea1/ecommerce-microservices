import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app, get_db
from app.db import Base
from app import models

# --- Configurare Centralizată ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_users.db"
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

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

# --- Date de Test ---
user_data = {
    "email": "test@example.com",
    "password": "password123",
    "full_name": "Test User",
    "phone_number": "0700123456",
    "address": "Str. Test",
    "city": "Testville",
    "country": "Testland"
}

# --- Teste pentru Înregistrare ---

def test_register_user_success(client):
    """Testează înregistrarea cu succes a unui utilizator."""
    response = client.post("/register", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_data["email"]
    assert "hashed_password" not in data # Asigură-te că parola nu este returnată

def test_register_user_duplicate_email(client, db_session):
    """Testează eșecul înregistrării cu un email duplicat."""
    # 1. Creează un utilizator inițial
    client.post("/register", json=user_data)
    
    # 2. Încearcă să creezi din nou același utilizator
    response = client.post("/register", json=user_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Acest email este deja înregistrat."

# --- Teste pentru Confirmare Cont ---

def test_confirm_account_success(client, db_session):
    """Testează confirmarea cu succes a unui cont."""
    # 1. Înregistrează un utilizator
    client.post("/register", json=user_data)
    
    # 2. Preluăm tokenul de confirmare direct din DB pentru test
    user = db_session.query(models.DBUser).filter_by(email=user_data["email"]).first()
    assert user is not None
    assert user.is_active is False
    confirmation_token = user.confirmation_token
    
    # 3. Facem request la endpoint-ul de confirmare
    response = client.get(f"/confirm/{confirmation_token}")
    assert response.status_code == 200
    
    # 4. Verificăm în DB că user-ul este acum activ
    db_session.refresh(user)
    assert user.is_active is True
    assert user.confirmation_token is None

# --- Teste pentru Login ---

def test_login_success(client, db_session):
    """Testează login-ul cu succes pentru un utilizator activ."""
    # 1. Înregistrează și activează un utilizator
    client.post("/register", json=user_data)
    user = db_session.query(models.DBUser).filter_by(email=user_data["email"]).first()
    confirmation_token = user.confirmation_token
    client.get(f"/confirm/{confirmation_token}")
    
    # 2. Încearcă să te loghezi
    login_data = {"username": user_data["email"], "password": user_data["password"]}
    response = client.post("/login", data=login_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_inactive_account(client):
    """Testează eșecul login-ului pentru un cont neconfirmat."""
    # 1. Doar înregistrează utilizatorul, fără a-l activa
    client.post("/register", json=user_data)
    
    # 2. Încearcă să te loghezi
    login_data = {"username": user_data["email"], "password": user_data["password"]}
    response = client.post("/login", data=login_data)
    
    assert response.status_code == 403
    assert response.json()["detail"] == "Contul nu este activat. Verifică-ți email-ul."

def test_login_incorrect_password(client):
    """Testează eșecul login-ului cu o parolă greșită."""
    client.post("/register", json=user_data) # Contul nu trebuie să fie activ pentru acest test
    
    login_data = {"username": user_data["email"], "password": "wrongpassword"}
    response = client.post("/login", data=login_data)
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"