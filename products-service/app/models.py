from sqlalchemy import Column, Integer, String, Float
from .db import Base
from pydantic import BaseModel


# Modelul SQLAlchemy (defineste tabelul din baza de date)
class DBProduct(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    stock = Column(Integer)


# Modelele Pydantic (definesc cum arata datele in API)
class ProductBase(BaseModel):
    name: str
    description: str | None = None
    price: float
    stock: int


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True
