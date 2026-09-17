from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models.document import Document


ALLOWED_MIME_TYPES = {
    "application/pdf": ".pdf",
    "image/jpeg": ".jpg",
    "image/png": ".png",
}

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".jpg",
    ".jpeg",
    ".png",
}

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


def save_uploaded_document(
    db: Session,
    file: UploadFile,
    property_id: int | None,
    upload_directory: Path,
) -> Document:

    original_filename = file.filename or ""

    original_extension = Path(original_filename).suffix.lower()

    if original_extension not in ALLOWED_EXTENSIONS:
        raise ValueError(
            "Unsupported file extension. "
            "Only PDF, JPG, JPEG and PNG files are allowed."
        )

    if file.content_type not in ALLOWED_MIME_TYPES:
        raise ValueError(
            "Unsupported file type. "
            "Only PDF, JPG, JPEG and PNG files are allowed."
        )

    file_extension = ALLOWED_MIME_TYPES[file.content_type]

    safe_filename = f"{uuid4().hex}{file_extension}"

    upload_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_path = upload_directory / safe_filename

    total_size = 0

    try:
        with file_path.open("wb") as buffer:
            while True:
                chunk = file.file.read(1024 * 1024)

                if not chunk:
                    break

                total_size += len(chunk)

                if total_size > MAX_FILE_SIZE:
                    raise ValueError(
                        "File size cannot exceed 10 MB."
                    )

                buffer.write(chunk)

    except ValueError:
        if file_path.exists():
            file_path.unlink()

        raise

    except Exception:
        if file_path.exists():
            file_path.unlink()

        raise

    document = Document(
        property_id=property_id,
        file_name=original_filename or safe_filename,
        file_path=str(file_path),
        document_type=None,
        mime_type=file.content_type,
        processing_status="uploaded",
    )

    try:
        db.add(document)
        db.commit()
        db.refresh(document)

    except Exception:
        db.rollback()

        if file_path.exists():
            file_path.unlink()

        raise

    return document