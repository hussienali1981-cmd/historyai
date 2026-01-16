from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .db import get_db
from . import models
from .schemas import JobCreate, JobOut
from .auth import get_current_user
from .jobs import enqueue_job

router = APIRouter()

@router.post("/jobs", response_model=JobOut)
def create_job(payload: JobCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    job = models.Job(
        user_id=user.id,
        topic=payload.topic,
        language=payload.language,
        duration_minutes=payload.duration_minutes,
        status="queued"
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    enqueue_job(job.id)
    return JobOut(id=job.id, topic=job.topic, status=job.status, result_path=job.result_path, error=job.error)

@router.get("/jobs/{job_id}", response_model=JobOut)
def get_job(job_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    job = db.query(models.Job).filter(models.Job.id == job_id, models.Job.user_id == user.id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobOut(id=job.id, topic=job.topic, status=job.status, result_path=job.result_path, error=job.error)
