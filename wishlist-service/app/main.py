import os
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import FastAPI, Depends, HTTPException, status, Security
from fastapi.security import APIKeyHeader
from jose import JWTError, jwt

from . import models, db

# --- Configurare ---
models.Base.metadata.create_all(bind=db.engine)

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")

app = FastAPI(title="Wishlist Service")

api_key_header_scheme = APIKeyHeader(name="Authorization")

# --- Dependințe (rămân neschimbate) ---
def get_db():
    database = db.SessionLocal()
    try:
        yield database
    finally:
        database.close()

async def get_current_user_email(token: str = Security(api_key_header_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    if not token.startswith("Bearer "):
        raise credentials_exception
    token = token.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        return email
    except JWTError:
        raise credentials_exception

# --- Endpoints API (CU CORECTURI) ---

@app.post("/wishlist", response_model=models.WishlistItem, status_code=status.HTTP_201_CREATED)
def add_to_wishlist(
    item_data: models.WishlistItemCreate,
    db: Session = Depends(get_db),
    user_email: str = Depends(get_current_user_email)
):
    """Adaugă un produs în wishlist-ul utilizatorului autentificat."""
    new_item = models.DBWishlistItem(
        user_email=user_email,
        product_id=item_data.product_id
    )
    db.add(new_item)
    try:
        db.commit()
        db.refresh(new_item)
        return new_item
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Produsul este deja în wishlist."
        )

@app.get("/wishlist", response_model=List[models.WishlistItem])
def get_wishlist(
    db: Session = Depends(get_db),
    user_email: str = Depends(get_current_user_email)
):
    """Returnează toate produsele din wishlist-ul utilizatorului."""
    return db.query(models.DBWishlistItem).filter(models.DBWishlistItem.user_email == user_email).all()

@app.delete("/wishlist/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_wishlist(
    product_id: int,
    db: Session = Depends(get_db),
    user_email: str = Depends(get_current_user_email)
):
    """Șterge un produs din wishlist."""
    item_to_delete = db.query(models.DBWishlistItem).filter(
        models.DBWishlistItem.user_email == user_email,
        models.DBWishlistItem.product_id == product_id
    ).first()

    if not item_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produsul nu a fost găsit în wishlist."
        )

    db.delete(item_to_delete)
    db.commit()
    return