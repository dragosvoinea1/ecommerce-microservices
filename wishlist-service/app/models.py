from sqlalchemy import Column, Integer, String, UniqueConstraint
from pydantic import BaseModel
from .db import Base

# --- Model SQLAlchemy (Baza de Date) ---

class DBWishlistItem(Base):
    __tablename__ = "wishlist_items"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, index=True, nullable=False)
    product_id = Column(Integer, index=True, nullable=False)

    # Ne asigurăm că un utilizator nu poate adăuga același produs de mai multe ori
    __table_args__ = (UniqueConstraint('user_email', 'product_id', name='_user_product_uc'),)


# --- Modele Pydantic (API) ---

class WishlistItemCreate(BaseModel):
    product_id: int

class WishlistItem(BaseModel):
    id: int
    user_email: str
    product_id: int

    class Config:
        from_attributes = True 