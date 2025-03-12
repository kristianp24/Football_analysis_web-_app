import datetime
from sqlalchemy import Column, Integer, String, DateTime,ForeignKey
from .base import Base
from sqlalchemy.orm import relationship
class User(Base):
    __tablename__ = 'users' 
    id = Column(Integer, primary_key=True)
    full_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    hashed_password = Column(String(200), nullable=False)
    token = Column(String(200))  
    token_expiration = Column(DateTime)  
    created_at = Column(DateTime, default=datetime.datetime.now)  # Automatically set creation time
    updated_at = Column(DateTime, onupdate=datetime.datetime.now) 
    videos = relationship('Video', back_populates='user', cascade="all, delete", passive_deletes=True)

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email
        }
    
from .videos import Video

