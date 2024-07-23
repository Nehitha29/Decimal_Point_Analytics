from sqlalchemy.orm import Session
from . import models, schemas
from sqlalchemy import func

def get_book(db: Session, book_name: str):
    return db.query(models.Book).filter(func.lower(models.Book.name) == book_name.lower()).first()

def get_bookbyid(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()

def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(name=book.name, author=book.author, rating=book.rating,link = book.link)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book(db: Session, book_id: int, book: schemas.Book):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book:
        db_book.name = book.name
        db_book.author = book.author
        db_book.rating = (book.rating + db_book.rating*db_book.persons)/(db_book.persons+1)
        db_book.persons = db_book.persons+1
        db.commit()
        db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book:
        db.delete(db_book)
        db.commit()
    return db_book
