from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DocumentUploadResponse(BaseModel):
    id: int
    property_id: int | None
    file_name: str
    file_path: str
    document_type: str | None
    mime_type: str | None
    processing_status: str
    uploaded_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)