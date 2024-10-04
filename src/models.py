import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    full_name = Column(String(100))
    profile_picture = Column(String(250))
    bio = Column(Text)
    
    posts = relationship('Post', back_populates='user')
    comments = relationship('Comment', back_populates='user')
    followers = relationship('Follower', foreign_keys='Follower.user_id', back_populates='user')
    following = relationship('Follower', foreign_keys='Follower.follower_id', back_populates='follower')

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    image_url = Column(String(250), nullable=False)
    caption = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship('User', back_populates='posts')
    comments = relationship('Comment', back_populates='post')

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('post.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')

class Follower(Base):
    __tablename__ = 'follower'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    follower_id = Column(Integer, ForeignKey('user.id'))

    user = relationship('User', foreign_keys=[user_id], back_populates='followers')
    follower = relationship('User', foreign_keys=[follower_id], back_populates='following')

try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem generating the diagram")
    raise e
