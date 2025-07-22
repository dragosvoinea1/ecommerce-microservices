from sqlalchemy import Column, Integer, String
from .db import Base
from pydantic import BaseModel, EmailStr


# Model SQLAlchemy (tabelul 'users')
class DBUser(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)


# Modele Pydantic (datele din API)
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class User(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True
