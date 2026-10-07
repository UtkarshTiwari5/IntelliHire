# ============================================================
# IntelliHire V7 - FastAPI Backend
# ============================================================

from fastapi import FastAPI
from sqlalchemy import text
from api.database import engine
from api import models
from api.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from api.jobs import router as jobs_router
from api.applications import router as applications_router
from api.interview import router as interview_router


# ============================================================
# CREATE API
# ============================================================

app = FastAPI(
    title="IntelliHire API",
    description=(
        "AI-powered Resume Analysis, "
        "Job Matching and Career Intelligence API"
    ),
    version="7.0.0"
)

app.include_router(
    auth_router
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "https://intellihire-cy87.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(jobs_router)
app.include_router(applications_router)
app.include_router(interview_router)



# ============================================================
# CREATE DATABASE TABLES
# ============================================================

models.Base.metadata.create_all(
    bind=engine
)


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():

    return {
        "project": "IntelliHire",
        "version": "V7",
        "status": "running",
        "message": "IntelliHire FastAPI backend is working."
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }

# ============================================================
# DATABASE HEALTH CHECK
# ============================================================

@app.get("/db-health")
def database_health():

    try:

        with engine.connect() as connection:

            connection.execute(
                text("SELECT 1")
            )

        return {
            "database": "PostgreSQL",
            "status": "connected"
        }

    except Exception as error:

        return {
            "database": "PostgreSQL",
            "status": "error",
            "message": str(error)
        }