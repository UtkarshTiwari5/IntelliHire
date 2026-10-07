from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from api.database import get_db
from api.models import User, Job, Application
from api.auth import require_role


router = APIRouter(
    prefix="/applications",
    tags=["Applications"]
)


# ============================================================
# APPLICATION REQUEST
# ============================================================

class ApplicationCreate(BaseModel):
    job_id: int


class ApplicationStatusUpdate(BaseModel):
    status: str


# ============================================================
# APPLY FOR JOB
# ============================================================

@router.post("/")
def apply_for_job(
    application_data: ApplicationCreate,
    current_user: User = Depends(require_role("user")),
    db: Session = Depends(get_db)
):

    job = db.query(Job).filter(
        Job.id == application_data.job_id
    ).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found."
        )

    existing_application = db.query(
        Application
    ).filter(
        Application.user_id == current_user.id,
        Application.job_id == application_data.job_id
    ).first()

    if existing_application:
        raise HTTPException(
            status_code=400,
            detail="You have already applied for this job."
        )

    new_application = Application(
        user_id=current_user.id,
        job_id=application_data.job_id,
        status="applied"
    )

    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    return {
        "message": "Application submitted successfully",
        "application": {
            "id": new_application.id,
            "user_id": new_application.user_id,
            "job_id": new_application.job_id,
            "status": new_application.status
        }
    }


# ============================================================
# GET MY APPLICATIONS
# ============================================================

@router.get("/my-applications")
def get_my_applications(
    current_user: User = Depends(require_role("user")),
    db: Session = Depends(get_db)
):

    applications = db.query(
        Application
    ).filter(
        Application.user_id == current_user.id
    ).order_by(
        Application.created_at.desc()
    ).all()

    return {
        "applications": [
            {
                "id": application.id,
                "user_id": application.user_id,
                "job_id": application.job_id,
                "status": application.status,
                "created_at": application.created_at
            }
            for application in applications
        ]
    }


# ============================================================
# GET RECRUITER APPLICATIONS
# ============================================================

@router.get("/recruiter-applications")
def get_recruiter_applications(
    current_user: User = Depends(require_role("recruiter")),
    db: Session = Depends(get_db)
):

    jobs = db.query(
        Job
    ).filter(
        Job.recruiter_id == current_user.id
    ).all()

    job_ids = [
        job.id
        for job in jobs
    ]

    if not job_ids:
        return {
            "applications": []
        }

    applications = db.query(
        Application
    ).filter(
        Application.job_id.in_(job_ids)
    ).order_by(
        Application.created_at.desc()
    ).all()

    return {
        "applications": [
            {
                "id": application.id,
                "user_id": application.user_id,
                "job_id": application.job_id,
                "status": application.status,
                "created_at": application.created_at
            }
            for application in applications
        ]
    }


# ============================================================
# UPDATE APPLICATION STATUS
# ============================================================

@router.put("/{application_id}/status")
def update_application_status(
    application_id: int,
    status_data: ApplicationStatusUpdate,
    current_user: User = Depends(require_role("recruiter")),
    db: Session = Depends(get_db)
):

    application = (
        db.query(Application)
        .join(Job, Application.job_id == Job.id)
        .filter(
            Application.id == application_id,
            Job.recruiter_id == current_user.id
        )
        .first()
    )

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found."
        )

    if status_data.status not in ["accepted", "rejected"]:
        raise HTTPException(
            status_code=400,
            detail="Status must be accepted or rejected."
        )

    application.status = status_data.status

    db.commit()
    db.refresh(application)

    return {
        "message": "Application status updated successfully.",
        "application": {
            "id": application.id,
            "job_id": application.job_id,
            "user_id": application.user_id,
            "status": application.status
        }
    }


# ============================================================
# RECRUITER - VIEW APPLICANTS
# ============================================================

@router.get("/recruiter-applicants")
def get_recruiter_applicants(
    current_user: User = Depends(require_role("recruiter")),
    db: Session = Depends(get_db)
):

    applications = (
        db.query(Application)
        .join(Job, Application.job_id == Job.id)
        .join(User, Application.user_id == User.id)
        .filter(
            Job.recruiter_id == current_user.id
        )
        .order_by(
            Application.created_at.desc()
        )
        .all()
    )

    return {
        "applications": [
            {
                "id": application.id,
                "job_id": application.job_id,
                "job_title": application.job.title
                if application.job else "Unknown",

                "applicant_id": application.user_id,
                "applicant_name": application.user.name
                if application.user else "Unknown",

                "applicant_email": application.user.email
                if application.user else "Unknown",

                "status": application.status,
                "created_at": application.created_at
            }
            for application in applications
        ]
    }