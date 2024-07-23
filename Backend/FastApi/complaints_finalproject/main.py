from fastapi import FastAPI, Form, UploadFile, File, Depends , status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Text, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Optional
from pydantic import BaseModel
import shutil
import os
from datetime import datetime
from secrets import token_hex

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:5500"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = "sqlite:///./complaints.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Complaint(Base):
    __tablename__ = "complaints"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    phone_number = Column(String, index=True)
    alternate_number = Column(String, index=True)
    email = Column(String, index=True)
    complaint_type = Column(String, index=True)
    source_of_purchase = Column(String, index=True)
    product_type = Column(String, index=True)
    product_name = Column(String, index=True)
    date_of_purchase = Column(Date, index=True)
    invoice_path = Column(String,index= True)
    # product_image_path = Column(String, index=True)
    # video_of_issue_path = Column(String, index=True)
    issue_details = Column(Text, index=True)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/submit_complaint")
async def submit_complaint(
    first_name: str = Form(...),
    last_name: str = Form(...),
    phone_number: str = Form(...),
    alternate_number: Optional[str] = Form(None),
    email: str = Form(...),
    complaint_type: str = Form(...),
    source_of_purchase: Optional[str] = Form(None),
    product_type: str = Form(...),
    product_name: str = Form(...),
    date_of_purchase: str = Form(...),
    invoice: UploadFile = File(...),
    # product_image: Optional[UploadFile] = File(None),
    # video_of_issue: Optional[UploadFile] = File(None),
    issue_details: str = Form(...),
    db: Session = Depends(get_db)
):
#     Convert the date_of_purchase string to a datetime.date object
    try:
        date_of_purchase = datetime.strptime(date_of_purchase, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")


   

    invoice_path = None
    
    invoice_ext = invoice.filename.split(".").pop()
    file_name = token_hex(10)
    file_path = f"{file_name}.{invoice_ext}"
    invoice_path = file_path
    with open(file_path, "wb") as buffer:
        content = await invoice.read()
        buffer.write(content)
            
    # product_image_path = None
    # if product_image:
    #     product_image_path = os.path.join(upload_directory, product_image.filename)
    #     with open(product_image_path, "wb") as buffer:
    #         shutil.copyfileobj(product_image.file, buffer)

    # video_of_issue_path = None
    # if video_of_issue:
    #     video_of_issue_path = os.path.join(upload_directory, video_of_issue.filename)
    #     with open(video_of_issue_path, "wb") as buffer:
    #         shutil.copyfileobj(video_of_issue.file, buffer)

    complaint = Complaint(
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number,
        alternate_number=alternate_number,
        email=email,
        complaint_type=complaint_type,
        source_of_purchase=source_of_purchase,
        product_type=product_type,
        product_name=product_name,
        date_of_purchase=date_of_purchase,
        invoice_path=file_path,
        # product_image_path=product_image_path,
        # video_of_issue_path=video_of_issue_path,
        issue_details=issue_details
    )

    db.add(complaint)
    db.commit()
    db.refresh(complaint)

    return { "message": "Complaint registered successfully!"}


