from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import crud, models, schemas
from .database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
models.Base.metadata.create_all(bind=engine)

app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/clothes/", response_model=schemas.Clothes)
def create_clothes(clothes: schemas.ClothesCreate, db: Session = Depends(get_db)):
    return crud.create_clothes(db=db, clothes=clothes)

@app.get("/clothes/", response_model=List[schemas.Clothes])
def read_all_clothes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    clothes = crud.get_all_clothes(db, skip=skip, limit=limit)
    return clothes

@app.get("/clothes/{clothes_id}", response_model=schemas.Clothes)
def read_clothes(clothes_id: int, db: Session = Depends(get_db)):
    db_clothes = crud.get_clothes(db, clothes_id=clothes_id)
    if db_clothes is None:
        raise HTTPException(status_code=404, detail="Clothes not found")
    return db_clothes

@app.get("/clothes/name/{clothes_name}", response_model=schemas.Clothes)
def read_clothes(clothes_name: str, db: Session = Depends(get_db)):
    db_clothes = crud.get_clothesbyname(db, clothes_name=clothes_name)
    if db_clothes is None:
        raise HTTPException(status_code=404, detail="Clothes not found")
    return db_clothes

@app.put("/clothes/{clothes_id}", response_model=schemas.Clothes)
def update_clothes(clothes_id: int, clothes: schemas.ClothesUpdate, db: Session = Depends(get_db)):
    db_clothes = crud.update_clothes(db, clothes_id=clothes_id, clothes=clothes)
    if db_clothes is None:
        raise HTTPException(status_code=404, detail="Clothes not found")
    return db_clothes

@app.delete("/clothes/{clothes_id}", response_model=schemas.Clothes)
def delete_clothes(clothes_id: int, db: Session = Depends(get_db)):
    db_clothes = crud.delete_clothes(db, clothes_id=clothes_id)
    if db_clothes is None:
        raise HTTPException(status_code=404, detail="Clothes not found")
    return db_clothes
