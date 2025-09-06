from sqlalchemy import Column, Integer, String
from .db import Base
from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, Integer, String, Boolean, DateTime # <-- Importă Boolean și DateTime
from typing import Optional


# Model SQLAlchemy (tabelul 'users')
class DBUser(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default = "user")
    full_name = Column(String, index=True)
    phone_number = Column(String, unique=True, index=True)
    address = Column(String)
    city = Column(String)
    country = Column(String)
    # email confirmation
    is_active = Column(Boolean, default=False)
    confirmation_token = Column(String, unique=True, index=True, nullable=True)
    token_expiration = Column(DateTime, nullable=True)

# Modele Pydantic (datele din API)
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    phone_number: str
    address: str
    city: str
    country: str


class User(BaseModel):
    id: int
    email: EmailStr
    role: str
    full_name: str
    phone_number: str
    address: str
    city: str
    country: str

    class Config:
        from_attributes = True
