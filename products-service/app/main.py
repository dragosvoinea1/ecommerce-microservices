from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
import os

from . import models, db
from .dependencies import get_current_admin_user

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
def create_category(category_data: models.CategoryCreate,
                    db: Session = Depends(get_db),
                    admin_user: dict = Depends(get_current_admin_user)):
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


@app.post("/", response_model=models.Product, status_code=201)
def create_product(product_data: models.ProductCreate,
                   db: Session = Depends(get_db),
                   admin_user: dict = Depends(get_current_admin_user)):
    """Creează un produs nou. Necesită rol de admin."""

    new_product = models.DBProduct(name=product_data.name,
                                   description=product_data.description,
                                   price=product_data.price,
                                   stock=product_data.stock,
                                   image_url=product_data.image_url,
                                   category_id=product_data.category_id)

    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@app.get("", response_model=List[models.Product])
def get_all_products(db: Session = Depends(get_db)):
    """Returneaza o lista cu toate produsele din baza de date."""
    return db.query(models.DBProduct).options(
        joinedload(models.DBProduct.category)).all()


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
    products = db.query(models.DBProduct).options(
        joinedload(models.DBProduct.category)).filter(
            models.DBProduct.category_id == category_id).all()
    if not products:
        # Chiar dacă nu există produse, o listă goală este un răspuns valid
        return []
    return products


@app.delete("/categories/{category_id}",
            status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int,
                    db: Session = Depends(get_db),
                    admin_user: dict = Depends(get_current_admin_user)):
    """Șterge o categorie. Necesită rol de admin."""
    category_to_delete = db.query(
        models.DBCategory).filter(models.DBCategory.id == category_id).first()

    if not category_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Categoria nu a fost găsită.")

    # Verificăm dacă există produse în această categorie
    if category_to_delete.products:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=
            "Nu poți șterge o categorie care conține produse. Mută sau șterge produsele mai întâi."
        )

    db.delete(category_to_delete)
    db.commit()
    return


@app.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int,
                   db: Session = Depends(get_db),
                   admin_user: dict = Depends(get_current_admin_user)):
    """Șterge un produs. Necesită rol de admin."""
    product_to_delete = db.query(
        models.DBProduct).filter(models.DBProduct.id == product_id).first()

    if not product_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Produsul nu a fost găsit.")

    db.delete(product_to_delete)
    db.commit()
    return


@app.put("/{product_id}", response_model=models.Product)
def update_product(product_id: int,
                   product_data: models.ProductUpdate,
                   db: Session = Depends(get_db),
                   admin_user: dict = Depends(get_current_admin_user)):
    """Actualizează un produs. Necesită rol de admin."""
    product_to_update = db.query(
        models.DBProduct).filter(models.DBProduct.id == product_id).first()

    if not product_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Produsul nu a fost găsit.")

    # Actualizăm doar câmpurile care au fost trimise în cerere
    update_data = product_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product_to_update, key, value)

    db.add(product_to_update)
    db.commit()
    db.refresh(product_to_update)
    return product_to_update
