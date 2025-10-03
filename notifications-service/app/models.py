from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from .db import Base
from pydantic import BaseModel
from datetime import datetime

# Model SQLAlchemy
class DBNotification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, index=True, nullable=False)
    message = Column(String, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# Model Pydantic
class Notification(BaseModel):
    id: int
    user_email: str
    message: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True