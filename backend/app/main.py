
from contextlib import asynccontextmanager
from app.land_record_router import router as land_record_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.audit import AuditLog
from app.land_record import LandRecord
from app.audit_router import router as audit_router
from app.dashboard_router import router as dashboard_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="LandIQ API",
    description="Land Record Digitization and Validation System",
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

app.include_router(audit_router)
app.include_router(dashboard_router)
app.include_router(land_record_router)


@app.get("/")
def root():
    return {"message": "LandIQ API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}