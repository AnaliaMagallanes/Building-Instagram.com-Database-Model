# src/models.py

from datetime import datetime
from sqlalchemy import String, Text, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# Declarative base
class Base(DeclarativeBase):
    pass

# User model
class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=True)
    profile_picture: Mapped[str] = mapped_column(String(250), nullable=True)
    bio: Mapped[str] = mapped_column(Text, nullable=True)

    posts: Mapped[list["Post"]] = relationship(back_populates='user')
    comments: Mapped[list["Comment"]] = relationship(back_populates='user')
    followers: Mapped[list["Follower"]] = relationship(
        foreign_keys='Follower.user_id', back_populates='user'
    )
    following: Mapped[list["Follower"]] = relationship(
        foreign_keys='Follower.follower_id', back_populates='follower'
    )

# Post model
class Post(Base):
    __tablename__ = 'post'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    image_url: Mapped[str] = mapped_column(String(250), nullable=False)
    caption: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates='posts')
    comments: Mapped[list["Comment"]] = relationship(back_populates='post')

# Comment model
class Comment(Base):
    __tablename__ = 'comment'

    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates='comments')
    post: Mapped["Post"] = relationship(back_populates='comments')

# Follower model
class Follower(Base):
    __tablename__ = 'follower'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    follower_id: Mapped[int] = mapped_column(ForeignKey('user.id'))

    user: Mapped["User"] = relationship(
        foreign_keys=[user_id], back_populates='followers'
    )
    follower: Mapped["User"] = relationship(
        foreign_keys=[follower_id], back_populates='following'
    )
