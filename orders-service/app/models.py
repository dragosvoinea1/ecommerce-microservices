from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base
from pydantic import BaseModel
from typing import List


# --- Model SQLAlchemy pentru Tabelul `orders` ---
class DBOrder(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    owner_email = Column(String, index=True)
    total_amount = Column(Float)

    items = relationship("DBOrderItem", back_populates="order")


# --- Model SQLAlchemy pentru Tabelul `order_items` ---
class DBOrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer)
    quantity = Column(Integer)
    price_at_purchase = Column(Float)
    order_id = Column(Integer, ForeignKey("orders.id"))

    order = relationship("DBOrder", back_populates="items")


# --- Modele Pydantic pentru API ---


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int


class OrderCreate(BaseModel):
    items: List[OrderItemBase]


class OrderItem(OrderItemBase):
    id: int
    price_at_purchase: float

    class Config:
        from_attributes = True


class Order(BaseModel):
    id: int
    owner_email: str
    total_amount: float
    items: List[OrderItem]

    class Config:
        from_attributes = True
