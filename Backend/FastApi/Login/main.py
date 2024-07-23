from fastapi import FastAPI, Form , APIRouter,Depends,status,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uvicorn

app = FastAPI()

# CORS middleware to allow communication with the frontend
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

DATABASE_URL = "sqlite:///./test2.db"

engine = create_engine(DATABASE_URL)
metadata = MetaData()
Base = declarative_base()

Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@app.post("/login")
async def login(email: str = Form(...), password: str = Form(...)):
    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if user.password != password:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    return {"message": "Login successful"}

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    phone_number = Column(String, unique=True, index=True) 


   
@app.post("/create_account")
async def create_account(email: str = Form(...), password: str = Form(...), phone_number: str = Form(...)):
    db = SessionLocal()
    user_email = db.query(User).filter(User.email == email).first()
    if user_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_phone = db.query(User).filter(User.phone_number == phone_number).first()
    if user_phone:
        raise HTTPException(status_code=400, detail="Phone number already registered")
    
    new_user = User(email=email, password=password, phone_number=phone_number)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Account created successfully"}



@app.post("/forgot_password")
async def forgot_password(email: str = Form(...),phone_number :str = Form(...)):
    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return {"message": "No account found with this email."}
    if user.phone_number != phone_number:
        raise HTTPException(status_code=400, detail="Invalid phone number")
    return {"password": user.password}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8008)

