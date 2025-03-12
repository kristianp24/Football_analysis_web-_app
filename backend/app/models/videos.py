from sqlalchemy import Column, Integer, BLOB, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Video(Base):
    __tablename__ = 'videos'
    id = Column(Integer, primary_key=True)
    video = Column(BLOB)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    user = relationship('User', back_populates='videos')

from .user import User