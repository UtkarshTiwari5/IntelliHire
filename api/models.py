# ============================================================
# IntelliHire V7.3 - Database Models
# ============================================================

from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship

from api.database import Base


# ============================================================
# USER MODEL
# ============================================================

class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = Column(
        String(255),
        nullable=False
    )

    role = Column(
        String(20),
        nullable=False,
        default="user"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    resumes = relationship(
        "Resume",
        back_populates="user"
    )

    applications = relationship(
        "Application",
        back_populates="user"
    )

    interviews = relationship(
        "Interview",
        back_populates="user"
    )


# ============================================================
# RESUME MODEL
# ============================================================

class Resume(Base):

    __tablename__ = "resumes"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    filename = Column(
        String(255),
        nullable=False
    )

    raw_text = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    user = relationship(
        "User",
        back_populates="resumes"
    )


# ============================================================
# JOB MODEL
# ============================================================

class Job(Base):

    __tablename__ = "jobs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    recruiter_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    title = Column(
        String(255),
        nullable=False
    )

    description = Column(
        Text,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    # --------------------------------------------------------
    # JOB -> APPLICATIONS RELATIONSHIP
    # --------------------------------------------------------

    applications = relationship(
        "Application",
        back_populates="job"
    )


# ============================================================
# APPLICATION MODEL
# ============================================================

class Application(Base):

    __tablename__ = "applications"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    job_id = Column(
        Integer,
        ForeignKey("jobs.id"),
        nullable=False
    )

    status = Column(
        String(50),
        default="applied"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    # --------------------------------------------------------
    # APPLICATION -> USER
    # --------------------------------------------------------

    user = relationship(
        "User",
        back_populates="applications"
    )

    # --------------------------------------------------------
    # APPLICATION -> JOB
    # --------------------------------------------------------

    job = relationship(
        "Job",
        back_populates="applications"
    )


# ============================================================
# INTERVIEW MODEL
# ============================================================

class Interview(Base):

    __tablename__ = "interviews"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    job_id = Column(
        Integer,
        ForeignKey("jobs.id"),
        nullable=True
    )

    score = Column(
        Integer,
        nullable=True
    )

    result = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    user = relationship(
        "User",
        back_populates="interviews"
    )
    questions = relationship(
    "InterviewQuestion",
    back_populates="interview",
    cascade="all, delete-orphan"
)

# ============================================================
# INTERVIEW QUESTION MODEL
# ============================================================

class InterviewQuestion(Base):

    __tablename__ = "interview_questions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    interview_id = Column(
        Integer,
        ForeignKey("interviews.id"),
        nullable=False
    )

    question = Column(
        Text,
        nullable=False
    )

    answer = Column(
        Text,
        nullable=True
    )

    score = Column(
        Integer,
        nullable=True
    )

    feedback = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    interview = relationship(
        "Interview",
        back_populates="questions"
    )