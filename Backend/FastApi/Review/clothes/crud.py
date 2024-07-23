from sqlalchemy.orm import Session
from . import models, schemas
from sqlalchemy import func

def get_clothes(db: Session, clothes_id: int):
    return db.query(models.Clothes).filter(models.Clothes.id == clothes_id).first()

def get_clothesbyname(db: Session, clothes_name: str):
    return db.query(models.Clothes).filter(func.lower(models.Clothes.material) == clothes_name.lower()).first()


def get_all_clothes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Clothes).offset(skip).limit(limit).all()

def create_clothes(db: Session, clothes: schemas.ClothesCreate):
    db_clothes = models.Clothes(material=clothes.material, type=clothes.type, rating=clothes.rating,link = clothes.link)
    db.add(db_clothes)
    db.commit()
    db.refresh(db_clothes)
    return db_clothes

def update_clothes(db: Session, clothes_id: int, clothes: schemas.ClothesUpdate):
    db_clothes = db.query(models.Clothes).filter(models.Clothes.id == clothes_id).first()
    if db_clothes:
        db_clothes.material = clothes.material
        db_clothes.type = clothes.type
        
        db_clothes.rating = (clothes.rating + db_clothes.rating*db_clothes.persons)/(db_clothes.persons+1)
        db_clothes.persons = db_clothes.persons+1
        db.commit()
        db.refresh(db_clothes)
    return db_clothes

def delete_clothes(db: Session, clothes_id: int):
    db_clothes = db.query(models.Clothes).filter(models.Clothes.id == clothes_id).first()
    if db_clothes:
        db.delete(db_clothes)
        db.commit()
    return db_clothes
