from fastapi import Depends, FastAPI, HTTPException
from typing import Optional
import requests
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

books_service = "http://localhost:8000"
clothes_service = "http://localhost:8001"




app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/search/{name}")
def search(name: str):
    try:
        # Attempt to find in books service
        response = requests.get(f"{books_service}/books/name/{name}")
        if response.status_code == 200:
            data = response.json()
            data['kind']='books'
            return data

        # Attempt to find in clothes service
        response = requests.get(f"{clothes_service}/clothes/name/{name}")
        if response.status_code == 200:
            data = response.json()
            data['kind']='clothes'

            return data

        # If not found in either service
        
    
    except :
        return {"message":"noting"}
