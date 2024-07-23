from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    author = Column(String)
    rating = Column(Float)
    persons = Column(Integer, default=1)
    link = Column(String)
    
