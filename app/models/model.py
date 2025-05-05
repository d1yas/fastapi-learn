# from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
# from sqlalchemy.orm import relationship
# from ..core.database import Base
# from datetime import datetime

# class Users(Base):
#     __tablename__ = 'users'

#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, unique=True, nullable=False)
#     email = Column(String, unique=True, nullable=False)
#     password = Column(String, nullable=False)
#     is_admin = Column(Boolean, default=False)
#     created_at = Column(DateTime, default=datetime.utcnow)

#     tickets = relationship("Ticket", back_populates="creator")
#     comments = relationship("Comment", back_populates="user")



# class Tickets(Base):
#     __tablename__ = 'tickets'

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, nullable=False)
#     description = Column(String, nullable=False)
#     status = Column(String, default='open')
#     priority = Column(String, default='medium')
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


#     user_id = Column(Integer, ForeignKey("users.id"))
#     creator = relationship("User", back_populates="tickets")

#     comments = relationship("Comment", back_populates="ticket", cascade="all, delete")
#     attachments = relationship("Attachment", back_populates="ticket", cascade="all, delete")



# class Comment(Base):
#     __tablename__ = "comments"

#     id = Column(Integer, primary_key=True, index=True)
#     content = Column(Text, nullable=False)
#     created_at = Column(DateTime, default=datetime.utcnow)

#     ticket_id = Column(Integer, ForeignKey("tickets.id"))
#     user_id = Column(Integer, ForeignKey("users.id"))

#     ticket = relationship("Ticket", back_populates="comments")
#     user = relationship("User", back_populates="comments")


# class Attachment(Base):
#     __tablename__ = "attachments"

#     id = Column(Integer, primary_key=True, index=True)
#     filename = Column(String, nullable=False)
#     file_path = Column(String, nullable=False)
#     uploaded_at = Column(DateTime, default=datetime.utcnow)

#     ticket_id = Column(Integer, ForeignKey("tickets.id"))
#     ticket = relationship("Ticket", back_populates="attachments")