from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.audit import AuditLog
from app.land_record import LandRecord

router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"],
)


@router.get("/metrics")
def get_dashboard_metrics(
    db: Session = Depends(get_db),
):
    total_records = db.query(LandRecord).count()

    verified_records = db.query(LandRecord).filter(
        LandRecord.status.ilike("Approved")
    ).count()

    requiring_verification = db.query(LandRecord).filter(
        LandRecord.status.ilike("Pending")
    ).count()

    validation_conflicts = db.query(LandRecord).filter(
        LandRecord.status.ilike("Rejected")
    ).count()

    documents_processed = db.query(AuditLog).filter(
        AuditLog.action == "Document Upload"
    ).count()

    return {
        "total_records": total_records,
        "documents_processed": documents_processed,
        "requiring_verification": requiring_verification,
        "validation_conflicts": validation_conflicts,
        "verified_records": verified_records,
        "average_confidence": 0,
    }