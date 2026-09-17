from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from app.database import get_db
from app.land_record import LandRecord

router = APIRouter(prefix="/api/land-records", tags=["Land Records"])


class LandRecordCreate(BaseModel):
    survey_number: str
    owner_name: str
    village: str
    taluka: str
    district: str
    land_area: float
    status: str = "Pending"


class LandRecordResponse(LandRecordCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)


@router.post("/", response_model=LandRecordResponse)
def create_land_record(data: LandRecordCreate, db: Session = Depends(get_db)):
    record = LandRecord(**data.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/", response_model=list[LandRecordResponse])
def get_land_records(db: Session = Depends(get_db)):
    return db.query(LandRecord).order_by(LandRecord.id.desc()).all()


@router.get("/{record_id}", response_model=LandRecordResponse)
def get_land_record(record_id: int, db: Session = Depends(get_db)):
    record = db.query(LandRecord).filter(LandRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Land record not found")
    return record


@router.put("/{record_id}", response_model=LandRecordResponse)
def update_land_record(
    record_id: int,
    data: LandRecordCreate,
    db: Session = Depends(get_db),
):
    record = db.query(LandRecord).filter(LandRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Land record not found")

    for field, value in data.model_dump().items():
        setattr(record, field, value)

    db.commit()
    db.refresh(record)
    return record


@router.delete("/{record_id}")
def delete_land_record(record_id: int, db: Session = Depends(get_db)):
    record = db.query(LandRecord).filter(LandRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Land record not found")

    db.delete(record)
    db.commit()
    return {"message": "Land record deleted"}