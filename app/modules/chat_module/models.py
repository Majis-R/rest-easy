from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    sender_username = Column(String(50), ForeignKey("users.username"), nullable=False)
    content = Column(String(500), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)