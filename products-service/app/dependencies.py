# products-service/app/dependencies.py

import os
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from jose import JWTError, jwt

# Preluăm setările pentru token din variabilele de mediu
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")

# Definim schema de securitate
api_key_header_scheme = APIKeyHeader(name="Authorization")

def get_current_admin_user(token: str = Depends(api_key_header_scheme)):
    """
    Validează token-ul și verifică dacă utilizatorul are rolul 'admin'.
    Dacă nu, ridică o excepție HTTP 403 Forbidden.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    forbidden_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User does not have admin privileges",
    )

    if not token.startswith("Bearer "):
        raise credentials_exception
    
    token = token.split(" ")[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        role: str = payload.get("role")
        if email is None or role is None:
            raise credentials_exception
        if role != "admin":
            raise forbidden_exception
    except JWTError:
        raise credentials_exception
    
    return {"email": email, "role": role}