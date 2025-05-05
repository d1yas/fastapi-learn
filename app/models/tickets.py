from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..core.database import Base
from datetime import datetime

class TicketsModel(Base):
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(String, default='open')
    priority = Column(String, default='medium')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    user_id = Column(Integer, ForeignKey("users.id"))
    creator = relationship("UsersModel", back_populates="tickets")

    comments = relationship("CommentsModel", back_populates="ticket")
    attachments = relationship("AttachmentsModel", back_populates="ticket")