
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.audit import AuditLog
router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"],
)


@router.get("/metrics")
def get_dashboard_metrics(
    db: Session = Depends(get_db),
):
    total_events = db.query(AuditLog).count()

    verified = db.query(AuditLog).filter(
        AuditLog.action == "Verification"
    ).count()

    uploads = db.query(AuditLog).filter(
        AuditLog.action == "Document Upload"
    ).count()

    return {
        "total_records": total_events,
        "documents_processed": uploads,
        "requiring_verification": 0,
        "validation_conflicts": 0,
        "verified_records": verified,
        "average_confidence": 0,
    }