from fastapi import FastAPI, Depends, HTTPException
from .db import engine, Base, get_db
from . import models
from .auth import get_password_hash, create_access_token, get_current_user, verify_password
from .schemas import UserCreate, Token
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from .workers import router as jobs_router
from fastapi.staticfiles import StaticFiles
import os

Base.metadata.create_all(bind=engine)

app = FastAPI(title="HistoryAI - Backend")

from .config import OUTPUT_DIR
os.makedirs(OUTPUT_DIR, exist_ok=True)
app.mount("/output", StaticFiles(directory=OUTPUT_DIR), name="output")

@app.post("/signup")
def signup(payload: UserCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == payload.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new = models.User(email=payload.email, hashed_password=get_password_hash(payload.password))
    db.add(new)
    db.commit()
    db.refresh(new)
    token = create_access_token({"sub": str(new.id)})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

app.include_router(jobs_router, prefix="/api")
