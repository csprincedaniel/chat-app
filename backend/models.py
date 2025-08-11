
from sqlalchemy import Column, Integer, String
from .db import Base

class User(Base):

    __tablename__ = "users"  # Name fo the table in the database

    id = Column(Integer, primary_key=True, index=True)
    Username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_passwords = Column(String, nullable=False)
    