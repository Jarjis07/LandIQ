from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from app.schemas.owner import OwnerResponse

class PropertyCreate(BaseModel):
    property_id: str = Field(min_length=1, max_length=100)
    survey_number: str = Field(min_length=1, max_length=100)
    village: str = Field(min_length=1, max_length=100)
    tehsil: str = Field(min_length=1, max_length=100)
    district: str = Field(min_length=1, max_length=100)
    state: str = Field(min_length=1, max_length=100)
    area: float | None = Field(default=None, gt=0)
    land_classification: str | None = Field(default=None, max_length=100)


class PropertyResponse(BaseModel):
    id: int
    property_id: str
    survey_number: str
    village: str
    tehsil: str
    district: str
    state: str
    area: float | None
    land_classification: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class PropertyUpdate(BaseModel):
    survey_number: str | None = Field(default=None, min_length=1, max_length=100)
    village: str | None = Field(default=None, min_length=1, max_length=100)
    tehsil: str | None = Field(default=None, min_length=1, max_length=100)
    district: str | None = Field(default=None, min_length=1, max_length=100)
    state: str | None = Field(default=None, min_length=1, max_length=100)
    area: float | None = Field(default=None, gt=0)
    land_classification: str | None = Field(default=None, max_length=100)

class PropertyProfileResponse(BaseModel):
    id: int
    property_id: str
    survey_number: str
    village: str
    tehsil: str
    district: str
    state: str
    area: float | None
    land_classification: str | None

    owners: list[OwnerResponse]
    total_ownership_percentage: float

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)