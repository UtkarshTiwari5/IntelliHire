# ============================================================
# IntelliHire V7.3 - Database Configuration
# ============================================================

import os

from dotenv import load_dotenv

from sqlalchemy import create_engine

from sqlalchemy.orm import (
    declarative_base,
    sessionmaker
)


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


DATABASE_URL = os.getenv(
    "DATABASE_URL"
)


# ============================================================
# VALIDATE DATABASE URL
# ============================================================

if not DATABASE_URL:

    raise RuntimeError(
        "DATABASE_URL is not configured in .env"
    )


# ============================================================
# DATABASE ENGINE
# ============================================================

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)


# ============================================================
# BASE MODEL
# ============================================================

Base = declarative_base()


# ============================================================
# DATABASE SESSION
# ============================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# ============================================================
# DATABASE DEPENDENCY
# ============================================================

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()