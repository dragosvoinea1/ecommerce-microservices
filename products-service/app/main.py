from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
import os

from . import models, db

# Creeaza tabelele in baza de date la pornirea aplicatiei
# (doar daca nu exista deja)
models.Base.metadata.create_all(bind=db.engine)

ROOT_PATH = os.environ.get("ROOT_PATH", "")
app = FastAPI(title="Products Service", root_path=ROOT_PATH)


# Functie pentru a obtine o sesiune de baza de date (Dependency Injection)
def get_db():
    database = db.SessionLocal()
    try:
        yield database
    finally:
        database.close()


@app.post("/categories", response_model=models.Category, status_code=201)
def create_category(category_data: models.CategoryCreate, db: Session = Depends(get_db)):
    """Creează o categorie nouă."""
    new_category = models.DBCategory(**category_data.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

@app.get("/categories", response_model=List[models.Category])
def get_all_categories(db: Session = Depends(get_db)):
    """Returnează o listă cu toate categoriile."""
    return db.query(models.DBCategory).all()


@app.post("", response_model=models.Product, status_code=201)
def create_product(product_data: models.ProductCreate,
                   db: Session = Depends(get_db)):
    """Creeaza un produs nou in baza de date."""
    new_product = models.DBProduct(**product_data.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@app.get("", response_model=List[models.Product])
def get_all_products(db: Session = Depends(get_db)):
    """Returneaza o lista cu toate produsele din baza de date."""
    return db.query(models.DBProduct).options(joinedload(models.DBProduct.category)).all()


@app.get("/{product_id}", response_model=models.Product)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    """Gaseste un produs dupa ID in baza de date."""
    product = db.query(models.DBProduct).options(
        joinedload(models.DBProduct.category)).filter(
            models.DBProduct.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.get("/category/{category_id}", response_model=List[models.Product])
def get_products_by_category(category_id: int, db: Session = Depends(get_db)):
    """Returnează o listă cu produsele dintr-o anumită categorie."""
    products = db.query(models.DBProduct).options(joinedload(models.DBProduct.category)).filter(models.DBProduct.category_id == category_id).all()
    if not products:
        # Chiar dacă nu există produse, o listă goală este un răspuns valid
        return []
    return products
