from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Clothes(Base):
    __tablename__ = "clothes"

    id = Column(Integer, primary_key=True, index=True)
    material = Column(String, index=True)
    type = Column(String)
    rating = Column(Float)
    persons = Column(Integer, default=1)
    link=Column(String)   
    
