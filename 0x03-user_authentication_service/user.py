#!/usr/bin/env python3
"""Users taple module"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Column


Base = declarative_base()


class User(Base):
    """Users table class"""
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True,)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    rest_token = Column(String(250), nullable=True)
