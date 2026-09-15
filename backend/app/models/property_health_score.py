from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class PropertyHealthScore(Base):
    __tablename__ = "property_health_scores"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    property_id: Mapped[int] = mapped_column(
        ForeignKey("properties.id"),
        nullable=False,
        unique=True,
        index=True,
    )

    score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    confidence_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    validation_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    verification_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    completeness_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="pending",
    )

    explanation: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    calculated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )