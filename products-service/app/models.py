from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base
from pydantic import BaseModel



class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True

# Modelele Pydantic (definesc cum arata datele in API)
class ProductBase(BaseModel):
    name: str
    description: str | None = None
    price: float
    stock: int


class ProductCreate(ProductBase):
    category_id: int


class Product(ProductBase):
    id: int
    category: Category

    class Config:
        from_attributes = True

class DBCategory(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    products = relationship("DBProduct", back_populates="category")


class DBProduct(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    stock = Column(Integer)

    category_id = Column(Integer,
                         ForeignKey("categories.id"))  # <-- Cheia externă
    category = relationship("DBCategory",
                            back_populates="products")  # <-- Relația
