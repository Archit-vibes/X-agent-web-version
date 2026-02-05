from sqlalchemy import Column, Integer, String, Text, Float
from sqlalchemy.sql import func

from db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    x_user_id = Column(String, unique=True, index=True, nullable=True)
    text = Column(String, nullable=True)


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True) 
    text = Column(Text, nullable=False)
    author_id = Column(String, index=True , nullable=True , default=None)



class FilteredPost(Base):
    __tablename__ = "filtered_posts"

    id = Column(Integer, primary_key=True)  
    text = Column(Text, nullable=False)
    author_id = Column(String, index=True)

    score = Column(Float, nullable=False)

class Reply(Base):
    __tablename__ = "replies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    target_tweet_id = Column(String, nullable=False, index=True)
    post_text = Column(Text, nullable=False)
    reply_text = Column(Text, nullable=False)
    status = Column(String, default="generated")



class Mention(Base):
    __tablename__ = "mentions"

    id = Column(Integer, primary_key=True) 
    text = Column(Text, nullable=False)
    author_id = Column(String, index=True)
