from fastapi import FastAPI
from sqlalchemy import text

from app.api.auth import router as auth_router
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
from app.api.documents import router as documents_router
from app.api.properties import router as properties_router



app = FastAPI(
    title="LandIQ API",
    description="Intelligent Land Record Digitization and Validation System",
    version="0.1.0",
)


Base.metadata.create_all(bind=engine)


app.include_router(auth_router)
app.include_router(properties_router)
app.include_router(documents_router)

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