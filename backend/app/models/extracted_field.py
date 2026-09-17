from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ExtractedField(Base):
    __tablename__ = "extracted_fields"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    document_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id"),
        nullable=False,
        index=True,
    )

    field_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    raw_value: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    normalized_value: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    confidence_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    extraction_method: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )