from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class JobCreate(BaseModel):
    topic: str
    language: Optional[str] = "ar"
    duration_minutes: Optional[int] = 12

class JobOut(BaseModel):
    id: int
    topic: str
    status: str
    result_path: Optional[str]
    error: Optional[str]
