# ============================================================
# IntelliHire V7 - Authentication Utilities
# ============================================================

import os

from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv

from jose import jwt

from passlib.context import CryptContext
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .models import (
    User,
    Resume,
    Application,
    Interview,
    Job
)


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


JWT_SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY"
)

JWT_ALGORITHM = os.getenv(
    "JWT_ALGORITHM",
    "HS256"
)

JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv(
        "JWT_ACCESS_TOKEN_EXPIRE_MINUTES",
        "60"
    )
)


# ============================================================
# PASSWORD HASHING
# ============================================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(
    password: str
) -> str:

    return pwd_context.hash(
        password
    )


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:

    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# ============================================================
# CREATE JWT ACCESS TOKEN
# ============================================================

def create_access_token(
    data: dict,
    expires_minutes: int | None = None
) -> str:

    to_encode = data.copy()

    expire_minutes = (
        expires_minutes
        if expires_minutes is not None
        else JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    )

    expire = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=expire_minutes
        )
    )

    to_encode.update(
        {
            "exp": expire
        }
    )

    return jwt.encode(
        to_encode,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )


# ============================================================
# DECODE JWT ACCESS TOKEN
# ============================================================

def decode_access_token(
    token: str
):

    return jwt.decode(
        token,
        JWT_SECRET_KEY,
        algorithms=[
            JWT_ALGORITHM
        ]
    )

# ============================================================
# V7 - REGISTER API
# ============================================================

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from api.database import SessionLocal
from api.models import User


# ============================================================
# AUTH ROUTER
# ============================================================

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

security = HTTPBearer()

# ============================================================
# DATABASE DEPENDENCY
# ============================================================

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# ============================================================
# REGISTER REQUEST
# ============================================================

class RegisterRequest(BaseModel):

    name: str

    email: EmailStr

    password: str

    role: str = "user"


# ============================================================
# REGISTER API
# ============================================================

@router.post("/register")
def register_user(
    user_data: RegisterRequest,
    db: Session = Depends(get_db)
):

    # --------------------------------------------------------
    # CHECK ROLE
    # --------------------------------------------------------

    allowed_roles = [
        "user",
        "recruiter"
    ]

    if user_data.role not in allowed_roles:

        raise HTTPException(
            status_code=400,
            detail="Invalid role. Use user or recruiter."
        )


    # --------------------------------------------------------
    # CHECK EXISTING EMAIL
    # --------------------------------------------------------

    existing_user = (
        db.query(User)
        .filter(
            User.email == user_data.email
        )
        .first()
    )

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already registered."
        )


    # --------------------------------------------------------
    # HASH PASSWORD
    # --------------------------------------------------------

    hashed_password = hash_password(
        user_data.password
    )


    # --------------------------------------------------------
    # CREATE USER
    # --------------------------------------------------------

    new_user = User(

        name=user_data.name,

        email=user_data.email,

        password_hash=hashed_password,

        role=user_data.role
    )


    # --------------------------------------------------------
    # SAVE TO DATABASE
    # --------------------------------------------------------

    db.add(
        new_user
    )

    db.commit()

    db.refresh(
        new_user
    )


    # --------------------------------------------------------
    # RESPONSE
    # --------------------------------------------------------

    return {

        "message": "User registered successfully.",

        "user": {

            "id": new_user.id,

            "name": new_user.name,

            "email": new_user.email,

            "role": new_user.role
        }
    }

# ============================================================
# V7.3 - LOGIN API
# ============================================================

from fastapi.security import OAuth2PasswordRequestForm


# ============================================================
# LOGIN API
# ============================================================

@router.post("/login")
def login_user(
    login_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    # --------------------------------------------------------
    # FIND USER
    # --------------------------------------------------------

    user = (
        db.query(User)
        .filter(
            User.email == login_data.username
        )
        .first()
    )

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )


    # --------------------------------------------------------
    # VERIFY PASSWORD
    # --------------------------------------------------------

    if not verify_password(
        login_data.password,
        user.password_hash
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )


    # --------------------------------------------------------
    # CREATE JWT TOKEN
    # --------------------------------------------------------

    access_token = create_access_token(
        {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role
        }
    )


    # --------------------------------------------------------
    # RESPONSE
    # --------------------------------------------------------

    return {

        "message": "Login successful.",

        "access_token": access_token,

        "token_type": "bearer",

        "user": {

            "id": user.id,

            "name": user.name,

            "email": user.email,

            "role": user.role
        }
    }

# ============================================================
# V7.5 - ROLE BASED ACCESS CONTROL
# ============================================================

from functools import wraps


# ============================================================
# ROLE CHECKER
# ============================================================

def require_role(required_role: str):

    def role_checker(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db)
    ):

        token = credentials.credentials

        try:

            payload = decode_access_token(
                token
            )

            user_id = payload.get(
                "sub"
            )

            if not user_id:

                raise HTTPException(
                    status_code=401,
                    detail="Invalid authentication token."
                )

        except Exception:

            raise HTTPException(
                status_code=401,
                detail="Invalid or expired authentication token."
            )


        user = (
            db.query(User)
            .filter(
                User.id == int(user_id)
            )
            .first()
        )

        if not user:

            raise HTTPException(
                status_code=404,
                detail="User not found."
            )


        if user.role != required_role:

            raise HTTPException(
                status_code=403,
                detail=(
                    f"Access denied. "
                    f"{required_role} role required."
                )
            )


        return user

    return role_checker

# ============================================================
# USER ONLY ENDPOINT
# ============================================================

@router.get("/user-area")
def user_area(
    current_user: User = Depends(
        require_role("user")
    )
):

    return {

        "message": "Welcome to User Area.",

        "user": {

            "id": current_user.id,

            "name": current_user.name,

            "email": current_user.email,

            "role": current_user.role
        }
    }

# ============================================================
# RECRUITER ONLY ENDPOINT
# ============================================================

@router.get("/recruiter-area")
def recruiter_area(
    current_user: User = Depends(
        require_role("recruiter")
    )
):

    return {

        "message": "Welcome to Recruiter Area.",

        "recruiter": {

            "id": current_user.id,

            "name": current_user.name,

            "email": current_user.email,

            "role": current_user.role
        }
    }

# ============================================================
# ADMIN ONLY ENDPOINT
# ============================================================

@router.get("/admin-area")
def admin_area(
    current_user: User = Depends(
        require_role("admin")
    )
):

    return {

        "message": "Welcome to Admin Area.",

        "admin": {

            "id": current_user.id,

            "name": current_user.name,

            "email": current_user.email,

            "role": current_user.role
        }
    }

# ============================================================
# V7.7 - CREATE ADMIN
# ============================================================

@router.post("/create-admin")
def create_admin(
    db: Session = Depends(get_db)
):

    admin_email = "admin@intellihire.com"

    existing_admin = (
        db.query(User)
        .filter(
            User.email == admin_email
        )
        .first()
    )

    if existing_admin:

        raise HTTPException(
            status_code=400,
            detail="Admin already exists."
        )

    hashed_password = hash_password(
        "Admin12345"
    )

    admin_user = User(

        name="IntelliHire Admin",

        email=admin_email,

        password_hash=hashed_password,

        role="admin"
    )

    db.add(
        admin_user
    )

    db.commit()

    db.refresh(
        admin_user
    )

    return {

        "message": "Admin created successfully.",

        "email": admin_user.email,

        "role": admin_user.role
    }

# ============================================================
# V7.7 - RESET ADMIN PASSWORD
# ============================================================

@router.post("/reset-admin-password")
def reset_admin_password(
    db: Session = Depends(get_db)
):

    admin = (
        db.query(User)
        .filter(
            User.email == "admin@intellihire.com"
        )
        .first()
    )

    if not admin:

        raise HTTPException(
            status_code=404,
            detail="Admin not found."
        )

    admin.password_hash = hash_password(
        "Admin12345"
    )

    admin.role = "admin"

    db.commit()

    return {
        "message": "Admin password reset successfully.",
        "email": admin.email,
        "role": admin.role
    }

# ============================================================
# V7.8 - USER DASHBOARD
# ============================================================

@router.get("/user-dashboard")
def user_dashboard(
    current_user: User = Depends(
        require_role("user")
    ),
    db: Session = Depends(get_db)
):

    # Count user's resumes
    resume_count = (
        db.query(Resume)
        .filter(
            Resume.user_id == current_user.id
        )
        .count()
    )

    # Count user's applications
    application_count = (
        db.query(Application)
        .filter(
            Application.user_id == current_user.id
        )
        .count()
    )

    # Count user's interviews
    interview_count = (
        db.query(Interview)
        .filter(
            Interview.user_id == current_user.id
        )
        .count()
    )

    return {

        "user": {
            "id": current_user.id,
            "name": current_user.name,
            "email": current_user.email,
            "role": current_user.role
        },

        "dashboard": {

            "resume_count": resume_count,

            "application_count": application_count,

            "interview_count": interview_count
        }
    }

# ============================================================
# V7.8 - RECRUITER DASHBOARD
# ============================================================

@router.get("/recruiter-dashboard")
def recruiter_dashboard(
    current_user: User = Depends(
        require_role("recruiter")
    ),
    db: Session = Depends(get_db)
):

    return {
        "recruiter": {
            "id": current_user.id,
            "name": current_user.name,
            "email": current_user.email,
            "role": current_user.role
        },

        "dashboard": {
            "total_jobs": 0,
            "total_applications": 0,
            "total_interviews": 0
        }
    }
# ============================================================
# V7.8 - ADMIN DASHBOARD
# ============================================================

@router.get("/admin-dashboard")
def admin_dashboard(
    current_user: User = Depends(
        require_role("admin")
    ),
    db: Session = Depends(get_db)
):

    total_users = (
        db.query(User)
        .count()
    )

    total_recruiters = (
        db.query(User)
        .filter(
            User.role == "recruiter"
        )
        .count()
    )

    total_jobs = (
        db.query(Job)
        .count()
    )

    total_resumes = (
        db.query(Resume)
        .count()
    )

    total_applications = (
        db.query(Application)
        .count()
    )

    total_interviews = (
        db.query(Interview)
        .count()
    )

    return {

        "admin": {
            "id": current_user.id,
            "name": current_user.name,
            "email": current_user.email,
            "role": current_user.role
        },

        "dashboard": {

            "total_users": total_users,

            "total_recruiters": total_recruiters,

            "total_jobs": total_jobs,

            "total_resumes": total_resumes,

            "total_applications": total_applications,

            "total_interviews": total_interviews
        }
    }