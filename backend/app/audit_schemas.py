
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AuditCreate(BaseModel):
    action: str = Field(min_length=1, max_length=100)
    user: str = Field(min_length=1, max_length=150)
    role: str = Field(min_length=1, max_length=100)

    entity_type: str = Field(min_length=1, max_length=100)
    entity_id: str = Field(min_length=1, max_length=150)

    field: str | None = None
    old_value: str | None = None
    new_value: str | None = None
    reason: str | None = None

    description: str = Field(min_length=1)


class AuditResponse(AuditCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    timestamp: datetime