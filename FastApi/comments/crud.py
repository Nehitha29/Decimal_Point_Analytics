from sqlalchemy.orm import Session
import models, schemas

def get_todo_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.ToDoItem).offset(skip).limit(limit).all()

def create_todo_item(db: Session, todo: schemas.ToDoItemCreate):
    db_todo = models.ToDoItem(title=todo.title, description=todo.description)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def get_todo_item(db: Session, todo_id: int):
    return db.query(models.ToDoItem).filter(models.ToDoItem.id == todo_id).first()

def update_todo_item(db: Session, todo_id: int, todo: schemas.ToDoItemCreate):
    db_todo = db.query(models.ToDoItem).filter(models.ToDoItem.id == todo_id).first()
    db_todo.title = todo.title
    db_todo.description = todo.description
    
    db.commit()
    db.refresh(db_todo)
    return db_todo

def delete_todo_item(db: Session, todo_id: int):
    db_todo = db.query(models.ToDoItem).filter(models.ToDoItem.id == todo_id).first()
    db.delete(db_todo)
    db.commit()
    return db_todo
