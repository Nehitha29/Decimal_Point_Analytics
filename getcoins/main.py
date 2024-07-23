from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


app = FastAPI()

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this based on your frontend's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class UserScore(Base):
    __tablename__ = "user_scores"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True)
    score = Column(Integer)

Base.metadata.create_all(bind=engine)

class ScoreRequest(BaseModel):
    userId: str
    score: int

@app.post("/save_score")
def save_score(request: ScoreRequest):
    session = SessionLocal()
    user_score = session.query(UserScore).filter(UserScore.user_id == request.userId).first()

    if user_score:
        user_score.score += request.score
    else:
        user_score = UserScore(user_id=request.userId, score=request.score)
        session.add(user_score)

    session.commit()
    session.close()

    return {"message": "Score saved successfully"}

@app.get("/get_scores")
def get_scores():
    session = SessionLocal()
    scores = session.query(UserScore).all()
    session.close()
    
    return scores

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
