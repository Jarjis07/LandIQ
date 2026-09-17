from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.core.database import Base, engine
from app.models import (
    Document,
    ExtractedField,
    Location,
    OCRResult,
    Owner,
    Property,
    PropertyBoundary,
    PropertyHealthScore,
    PropertyOwner,
    Role,
    User,
    ValidationResult,
    VerificationRecord,
)
from app.api.auth import router as auth_router
from app.api.documents import router as documents_router
from app.api.properties import router as properties_router

from app.database import Base as AuditBase, engine as audit_engine
from app.audit import AuditLog
from app.land_record import LandRecord
from app.audit_router import router as audit_router
from app.dashboard_router import router as dashboard_router
from app.land_record_router import router as land_record_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    AuditBase.metadata.create_all(bind=audit_engine)
    yield


app = FastAPI(
    title="LandIQ API",
    description="Intelligent Land Record Digitization and Validation System",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8081",
        "http://localhost:19006",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(properties_router)
app.include_router(documents_router)
app.include_router(audit_router)
app.include_router(dashboard_router)
app.include_router(land_record_router)


@app.get("/")
def root():
    return {
        "message": "LandIQ API is running",
        "version": "0.1.0",
        "status": "ok",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "landiq-backend",
    }


@app.get("/health/database")
def database_health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected",
        }

    except Exception as error:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(error),
        }