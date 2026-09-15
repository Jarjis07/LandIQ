from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.property import Property
from app.models.user import User
from app.schemas.document import DocumentUploadResponse
from app.services.document_service import save_uploaded_document


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


UPLOAD_DIRECTORY = Path(__file__).resolve().parents[2] / "uploads"


@router.post(
    "/upload",
    response_model=DocumentUploadResponse,
    status_code=status.HTTP_201_CREATED,
)
def upload_document(
    file: UploadFile = File(...),
    property_id: str | None = Form(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    property_record = None

    if property_id is not None:
        property_record = (
            db.query(Property)
            .filter(Property.property_id == property_id)
            .first()
        )

        if property_record is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Property not found",
            )

    try:
        document = save_uploaded_document(
            db=db,
            file=file,
            property_id=property_record.id if property_record else None,
            upload_directory=UPLOAD_DIRECTORY,
        )

        return document

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload document",
        )