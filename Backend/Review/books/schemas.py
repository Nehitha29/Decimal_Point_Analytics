from pydantic import BaseModel

class BookBase(BaseModel):
    name: str
    author: str
    rating: float


class BookCreate(BookBase):
    link:str
    
    pass

class BookUpdate(BookBase):
    
    
    pass

class Book(BookBase):
    id: int
    link:str

    class Config:
        orm_mode = True
