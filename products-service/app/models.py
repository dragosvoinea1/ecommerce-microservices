from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base
from pydantic import BaseModel
from typing import List, Optional

# --- Modele Pydantic ---

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int
    image_url: Optional[str] = None # Asigurăm că este aici
    discount_percentage: Optional[float] = None

class ProductCreate(ProductBase):
    category_id: int


class Product(ProductBase):  # Moștenește 'image_url' de la ProductBase
    id: int
    category: Category

    class Config:
        from_attributes = True

# Adaugă această clasă în products-service/app/models.py, alături de celelalte modele Pydantic


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    image_url: Optional[str] = None
    category_id: Optional[int] = None
    discount_percentage: Optional[float] = None

# --- Modele SQLAlchemy (Baza de Date) ---

class DBCategory(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    products = relationship("DBProduct", back_populates="category")


class DBProduct(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    price = Column(Float)
    stock = Column(Integer)
    image_url = Column(String, nullable=True)  # Asigurăm că este aici
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("DBCategory", back_populates="products")
    discount_percentage = Column(Float, nullable=True, default=0.0)