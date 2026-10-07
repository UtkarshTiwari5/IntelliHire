from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from api.database import get_db
from api.models import User, Job
from api.auth import require_role


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


# ============================================================
# JOB REQUEST
# ============================================================

class JobCreate(BaseModel):

    title: str

    description: str


# ============================================================
# CREATE JOB
# ============================================================

@router.post("/")
def create_job(
    job_data: JobCreate,
    current_user: User = Depends(
        require_role("recruiter")
    ),
    db: Session = Depends(get_db)
):

    new_job = Job(
        recruiter_id=current_user.id,
        title=job_data.title,
        description=job_data.description
    )

    db.add(new_job)

    db.commit()

    db.refresh(new_job)

    return {
        "message": "Job created successfully",
        "job": {
            "id": new_job.id,
            "title": new_job.title,
            "description": new_job.description,
            "recruiter_id": new_job.recruiter_id
        }
    }


# ============================================================
# GET ALL JOBS
# ============================================================

@router.get("/")
def get_jobs(
    db: Session = Depends(get_db)
):

    jobs = db.query(Job).order_by(
        Job.created_at.desc()
    ).all()

    return {
        "jobs": [
            {
                "id": job.id,
                "recruiter_id": job.recruiter_id,
                "title": job.title,
                "description": job.description,
                "created_at": job.created_at
            }
            for job in jobs
        ]
    }