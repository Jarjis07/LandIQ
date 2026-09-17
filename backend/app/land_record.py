from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class LandRecord(Base):
    __tablename__ = "land_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    survey_number: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    owner_name: Mapped[str] = mapped_column(String(150), nullable=False)
    village: Mapped[str] = mapped_column(String(150), nullable=False)
    taluka: Mapped[str] = mapped_column(String(150), nullable=False)
    district: Mapped[str] = mapped_column(String(150), nullable=False)
    land_area: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="Pending")