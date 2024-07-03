import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Enum, create_engine
from sqlalchemy.orm import relationship, declarative_base
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False)
    firstname = Column(String(250), nullable=False)
    lastname = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)

    posts = relationship('Post', back_populates='user')
    comments = relationship('Comment', back_populates='author')
    followers = relationship('Follower', back_populates='user_from', foreign_keys='Follower.user_from_id')
    followings = relationship('Follower', back_populates='user_to', foreign_keys='Follower.user_to_id')

class Follower(Base):
    __tablename__ = 'Follower'
    id = Column(Integer, primary_key=True)
    user_from_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    user_to_id = Column(Integer, ForeignKey('User.id'), nullable=False)

    user_from = relationship('User', foreign_keys=[user_from_id], back_populates='followers')
    user_to = relationship('User', foreign_keys=[user_to_id], back_populates='followings')

class Post(Base):
    __tablename__ = 'Post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)

    user = relationship('User', back_populates='posts')
    comments = relationship('Comment', back_populates='post')
    media = relationship('Media', back_populates='post')

class Media(Base):
    __tablename__ = 'Media'
    id = Column(Integer, primary_key=True)
    type = Column(String(50), nullable=False)
    url = Column(String(250), nullable=False)
    post_id = Column(Integer, ForeignKey('Post.id'), nullable=False)

    post = relationship('Post', back_populates='media')

class Comment(Base):
    __tablename__ = 'Comment'
    id = Column(Integer, primary_key=True)
    comment_text = Column(String(250), nullable=False)
    author_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('Post.id'), nullable=False)

    author = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')

    def to_dict(self):
        return {}

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("¡Éxito! Revisa el archivo diagram.png")
except Exception as e:
    print("Hay problemas para generar el diagrama")
    raise e
