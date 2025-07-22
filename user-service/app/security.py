import os
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import JWTError, jwt

# --- Configurarea pentru Parole ---
# Specificam algoritmul de hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    """Verifica daca parola simpla corespunde cu cea hash-uita."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """Returneaza hash-ul pentru o parola."""
    return pwd_context.hash(password)


# --- Configurarea pentru Token-uri JWT ---
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    """Creeaza un nou token de acces."""
    to_encode = data.copy()
    expire = datetime.now(
        timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
