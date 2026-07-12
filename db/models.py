from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base


class DbUser(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    items = relationship('DbPost', back_populates='user')
    comments = relationship('DbComment', back_populates='user')


class DbPost(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
    image_url_type = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('DbUser', back_populates='items')
    timestamp = Column(DateTime, nullable=False)
    comments = relationship('DbComment', back_populates='post')

class DbComment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    username = Column(String, nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    timestamp = Column(DateTime, nullable=False)

    user = relationship('DbUser', back_populates='comments')
    post = relationship('DbPost', back_populates='comments')
