import os
from typing import List

from fastapi import FastAPI, Depends, HTTPException, status, Security
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from . import models, db

# --- Configurare ---

# Creează tabelul `reviews` la pornire, dacă nu există
models.Base.metadata.create_all(bind=db.engine)

# Preluăm variabilele de mediu (le vom adăuga ulterior în docker-compose.yml)
ROOT_PATH = os.environ.get("ROOT_PATH", "")
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")

app = FastAPI(title="Reviews Service", root_path=ROOT_PATH)

# Schema pentru a extrage token-ul din header-ul "Authorization"
api_key_header_scheme = APIKeyHeader(name="Authorization")

# --- Dependințe ---

def get_db():
    """Funcție pentru a obține o sesiune de bază de date."""
    database = db.SessionLocal()
    try:
        yield database
    finally:
        database.close()

async def get_current_user_email(token: str = Security(api_key_header_scheme)):
    """
    Extrage token-ul din header, îl validează și returnează email-ul utilizatorului.
    Funcționează la fel ca în `orders-service`.
    """
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

# --- Endpoints API ---

@app.post("", response_model=models.Review, status_code=status.HTTP_201_CREATED)
def create_review(
    review_data: models.ReviewCreate,
    db: Session = Depends(get_db),
    user_email: str = Depends(get_current_user_email)
):
    """
    Creează o recenzie nouă pentru un produs.
    Doar utilizatorii autentificați pot adăuga recenzii.
    """
    # Validăm rating-ul să fie între 1 și 5
    if not 1 <= review_data.rating <= 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rating-ul trebuie să fie între 1 și 5."
        )

    # Creăm obiectul pentru baza de date
    new_review = models.DBReview(
        **review_data.dict(),
        user_email=user_email
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

@app.get("/product/{product_id}", response_model=List[models.Review])
def get_reviews_for_product(product_id: int, db: Session = Depends(get_db)):
    """
    Returnează o listă cu toate recenziile pentru un produs specific.
    Acest endpoint este public, nu necesită autentificare.
    """
    reviews = db.query(models.DBReview).filter(models.DBReview.product_id == product_id).all()
    return reviews

@app.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    user_email: str = Depends(get_current_user_email)
):
    """
    Șterge o recenzie.
    Doar utilizatorul care a creat recenzia o poate șterge.
    """
    review_to_delete = db.query(models.DBReview).filter(models.DBReview.id == review_id).first()

    if not review_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recenzia nu a fost găsită."
        )

    if review_to_delete.user_email != user_email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Nu ai permisiunea să ștergi această recenzie."
        )

    db.delete(review_to_delete)
    db.commit()
    return