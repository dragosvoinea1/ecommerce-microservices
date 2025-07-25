from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
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


@app.post("", response_model=models.Product, status_code=201)
def create_product(product_data: models.ProductCreate,
                   database: Session = Depends(get_db)):
    """Creeaza un produs nou in baza de date."""
    new_product = models.DBProduct(**product_data.dict())
    database.add(new_product)
    database.commit()
    database.refresh(new_product)
    return new_product


@app.get("", response_model=List[models.Product])
def get_all_products(database: Session = Depends(get_db)):
    """Returneaza o lista cu toate produsele din baza de date."""
    all_products = database.query(models.DBProduct).all()
    return all_products


@app.get("/{product_id}", response_model=models.Product)
def get_product_by_id(product_id: int, database: Session = Depends(get_db)):
    """Gaseste un produs dupa ID in baza de date."""
    product = database.query(
        models.DBProduct).filter(models.DBProduct.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
