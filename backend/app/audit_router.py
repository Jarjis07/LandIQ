
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.audit import AuditLog
from app.audit_schemas import AuditCreate, AuditResponse

router = APIRouter(prefix="/api", tags=["Audit Trail"])


@router.get(
    "/audit",
    response_model=list[AuditResponse],
)
def get_audit_logs(
    db: Session = Depends(get_db),
):
    return (
        db.query(AuditLog)
        .order_by(AuditLog.timestamp.desc())
        .limit(100)
        .all()
    )


@router.post(
    "/audit",
    response_model=AuditResponse,
    status_code=201,
)
def create_audit_log(
    payload: AuditCreate,
    db: Session = Depends(get_db),
):
    event = AuditLog(**payload.model_dump())

    try:
        db.add(event)
        db.commit()
        db.refresh(event)

        return event

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Unable to save audit event",
        )