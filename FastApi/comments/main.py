from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def read_todo_items(request: Request, db: Session = Depends(get_db)):
    todos = crud.get_todo_items(db)
    
    return templates.TemplateResponse("index.html", {"request": request, "todos": todos})

@app.get("/create/", response_class=HTMLResponse)
def create_todo_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/create/")
def create_todo(title: str = Form(...), description: str = Form(...), db: Session = Depends(get_db)):
    todo = schemas.ToDoItemCreate(title=title, description=description)
    crud.create_todo_item(db=db, todo=todo)
    return HTMLResponse(status_code=303, headers={"Location": "/"})

@app.get("/edit/{todo_id}", response_class=HTMLResponse)
def edit_todo_form(request: Request, todo_id: int, db: Session = Depends(get_db)):
    todo = crud.get_todo_item(db, todo_id=todo_id)
    return templates.TemplateResponse("form.html", {"request": request, "todo": todo})

@app.post("/edit/{todo_id}")
def update_todo(todo_id: int, title: str = Form(...), description: str = Form(...), completed: bool = Form(False), db: Session = Depends(get_db)):
    todo_data = schemas.ToDoItemCreate(title=title, description=description, completed=completed)
    crud.update_todo_item(db=db, todo_id=todo_id, todo=todo_data)
    return HTMLResponse(status_code=303, headers={"Location": "/"})

@app.get("/delete/{todo_id}")
def delete_todo_item(todo_id: int, db: Session = Depends(get_db)):
    crud.delete_todo_item(db=db, todo_id=todo_id)
    return HTMLResponse(status_code=303, headers={"Location": "/"})
