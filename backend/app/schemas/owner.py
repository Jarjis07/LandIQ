from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class OwnerCreate(BaseModel):
    full_name: str = Field(min_length=1, max_length=150)
    father_or_husband_name: str | None = Field(
        default=None,
        max_length=150,
    )
    address: str | None = Field(
        default=None,
        max_length=500,
    )
    ownership_type: str = Field(
        default="owner",
        min_length=1,
        max_length=50,
    )
    ownership_percentage: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )


class OwnerResponse(BaseModel):
    id: int
    full_name: str
    father_or_husband_name: str | None
    address: str | None
    ownership_type: str
    ownership_percentage: float | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class OwnerOwnershipUpdate(BaseModel):
    ownership_percentage: float = Field(
        ge=0,
        le=100,
    )