from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from fastapi.middleware.cors import CORSMiddleware

DATABASE_URL = "sqlite:///./test.db"

database = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=database)
Base = declarative_base()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
# Models
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    wishlists = relationship("Wishlist", back_populates="owner")

class Wishlist(Base):
    __tablename__ = "wishlists"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, index=True)
    item_name = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="wishlists")

# Schemas
class WishlistItemCreate(BaseModel):
    item_id: int
    item_name:str


class WishlistItem(BaseModel):
    id: int
    item_id: int
    item_name:str

    class Config:
        orm_mode = True

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize the database
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=database)

# Routes
@app.post("/users/{email}/wishlist/")
async def add_to_wishlist(email: str, wishlist_item: WishlistItemCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        user = User(email=email)
        db.add(user)
        db.commit()
        db.refresh(user)

    existing_item = db.query(Wishlist).filter(
        Wishlist.owner == user,
        Wishlist.item_id == wishlist_item.item_id
    ).first()
    
    if existing_item:
        # Return a message if the item already exists in the wishlist
        return {"message": "Item already in wishlist", "item_name": wishlist_item.item_name}
 
     
    wishlist_item_db = Wishlist(item_id=wishlist_item.item_id, owner=user,item_name = wishlist_item.item_name)
    db.add(wishlist_item_db)
    db.commit()
    db.refresh(wishlist_item_db)
    return {"email": email, "item_name": wishlist_item.item_name}

@app.get("/users/{email}/wishlist/", response_model=list[WishlistItem])
async def get_wishlist(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user.wishlists
