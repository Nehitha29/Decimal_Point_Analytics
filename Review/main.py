from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Book(BaseModel):
    id: int
    title: str
    author: str
    description: Optional[str] = None

class Clothes(BaseModel):
    id: int
    type: str
    size: str
    color: str
    description: Optional[str] = None

books = []
clothes = []

@app.post("/books/", response_model=Book)
def create_book(book: Book):
    books.append(book)
    return book

@app.get("/books/", response_model=List[Book])
def get_books():
    return books

@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, book: Book):
    for b in books:
        if b.id == book_id:
            b.title = book.title
            b.author = book.author
            b.description = book.description
            return b
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/{book_id}", response_model=Book)
def delete_book(book_id: int):
    for b in books:
        if b.id == book_id:
            books.remove(b)
            return b
    raise HTTPException(status_code=404, detail="Book not found")

@app.post("/clothes/", response_model=Clothes)
def create_clothes(item: Clothes):
    clothes.append(item)
    return item

@app.get("/clothes/", response_model=List[Clothes])
def get_clothes():
    return clothes

@app.put("/clothes/{clothes_id}", response_model=Clothes)
def update_clothes(clothes_id: int, item: Clothes):
    for c in clothes:
        if c.id == clothes_id:
            c.type = item.type
            c.size = item.size
            c.color = item.color
            c.description = item.description
            return c
    raise HTTPException(status_code=404, detail="Clothes not found")

@app.delete("/clothes/{clothes_id}", response_model=Clothes)
def delete_clothes(clothes_id: int):
    for c in clothes:
        if c.id == clothes_id:
            clothes.remove(c)
            return c
    raise HTTPException(status_code=404, detail="Clothes not found")
