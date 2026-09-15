from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_roles
from app.models.owner import Owner
from app.models.property import Property
from app.models.property_owner import PropertyOwner
from app.models.user import User
from app.schemas.owner import (
    OwnerCreate,
    OwnerOwnershipUpdate,
    OwnerResponse,
)
from app.schemas.property import (
    PropertyCreate,
    PropertyProfileResponse,
    PropertyResponse,
    PropertyUpdate,
)


router = APIRouter(
    prefix="/properties",
    tags=["Properties"],
)


@router.post(
    "/",
    response_model=PropertyResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_property(
    request: PropertyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("admin", "land_officer")
    ),
):
    existing_property = (
        db.query(Property)
        .filter(Property.property_id == request.property_id)
        .first()
    )

    if existing_property:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Property with this property_id already exists",
        )

    property_record = Property(
        property_id=request.property_id,
        survey_number=request.survey_number,
        village=request.village,
        tehsil=request.tehsil,
        district=request.district,
        state=request.state,
        area=request.area,
        land_classification=request.land_classification,
    )

    db.add(property_record)

    try:
        db.commit()
        db.refresh(property_record)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Property could not be created because of a database conflict",
        )

    return property_record


@router.get(
    "/{property_id}",
    response_model=PropertyResponse,
)
def get_property(
    property_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
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

    return property_record


@router.patch(
    "/{property_id}",
    response_model=PropertyResponse,
)
def update_property(
    property_id: str,
    request: PropertyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("admin", "land_officer")
    ),
):
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

    update_data = request.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(property_record, field, value)

    db.commit()
    db.refresh(property_record)

    return property_record


@router.post(
    "/{property_id}/owners",
    response_model=OwnerResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_property_owner(
    property_id: str,
    request: OwnerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("admin", "land_officer", "verifier")
    ),
):
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

    # Calculate existing ownership percentage
    existing_ownership_rows = (
        db.query(PropertyOwner)
        .filter(
            PropertyOwner.property_id == property_record.id
        )
        .all()
    )

    current_percentage = sum(
        row.ownership_percentage or 0
        for row in existing_ownership_rows
    )

    requested_percentage = request.ownership_percentage or 0

    # Prevent total ownership from exceeding 100%
    if current_percentage + requested_percentage > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Total ownership cannot exceed 100%. "
                f"Current ownership: {current_percentage}%, "
                f"requested: {requested_percentage}%."
            ),
        )

    owner = Owner(
        full_name=request.full_name,
        father_or_husband_name=request.father_or_husband_name,
        address=request.address,
    )

    db.add(owner)
    db.flush()

    property_owner = PropertyOwner(
        property_id=property_record.id,
        owner_id=owner.id,
        ownership_type=request.ownership_type,
        ownership_percentage=request.ownership_percentage,
    )

    db.add(property_owner)
    db.commit()
    db.refresh(owner)

    return {
        "id": owner.id,
        "full_name": owner.full_name,
        "father_or_husband_name": owner.father_or_husband_name,
        "address": owner.address,
        "ownership_type": property_owner.ownership_type,
        "ownership_percentage": property_owner.ownership_percentage,
        "created_at": owner.created_at,
    }


@router.get(
    "/{property_id}/owners",
    response_model=list[OwnerResponse],
)

@router.patch(
    "/{property_id}/owners/{owner_id}",
    response_model=OwnerResponse,
)
def update_owner_ownership(
    property_id: str,
    owner_id: int,
    request: OwnerOwnershipUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("admin", "land_officer", "verifier")
    ),
):
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

    property_owner = (
        db.query(PropertyOwner)
        .filter(
            PropertyOwner.property_id == property_record.id,
            PropertyOwner.owner_id == owner_id,
        )
        .first()
    )

    if property_owner is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Owner is not associated with this property",
        )

    other_ownership_rows = (
        db.query(PropertyOwner)
        .filter(
            PropertyOwner.property_id == property_record.id,
            PropertyOwner.owner_id != owner_id,
        )
        .all()
    )

    other_percentage = sum(
        row.ownership_percentage or 0
        for row in other_ownership_rows
    )

    if other_percentage + request.ownership_percentage > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Total ownership cannot exceed 100%. "
                f"Other owners: {other_percentage}%, "
                f"requested ownership: "
                f"{request.ownership_percentage}%."
            ),
        )

    property_owner.ownership_percentage = (
        request.ownership_percentage
    )

    db.commit()
    db.refresh(property_owner)

    owner = (
        db.query(Owner)
        .filter(Owner.id == owner_id)
        .first()
    )

    return {
        "id": owner.id,
        "full_name": owner.full_name,
        "father_or_husband_name": owner.father_or_husband_name,
        "address": owner.address,
        "ownership_type": property_owner.ownership_type,
        "ownership_percentage": property_owner.ownership_percentage,
        "created_at": owner.created_at,
    }
def get_property_owners(
    property_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
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

    owner_rows = (
        db.query(Owner, PropertyOwner)
        .join(
            PropertyOwner,
            PropertyOwner.owner_id == Owner.id,
        )
        .filter(
            PropertyOwner.property_id == property_record.id
        )
        .all()
    )

    return [
        {
            "id": owner.id,
            "full_name": owner.full_name,
            "father_or_husband_name": owner.father_or_husband_name,
            "address": owner.address,
            "ownership_type": property_owner.ownership_type,
            "ownership_percentage": property_owner.ownership_percentage,
            "created_at": owner.created_at,
        }
        for owner, property_owner in owner_rows
    ]

@router.get(
    "/{property_id}/profile",
    response_model=PropertyProfileResponse,
)
def get_property_profile(
    property_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
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

    owner_rows = (
        db.query(Owner, PropertyOwner)
        .join(
            PropertyOwner,
            PropertyOwner.owner_id == Owner.id,
        )
        .filter(
            PropertyOwner.property_id == property_record.id
        )
        .all()
    )

    owners = [
        {
            "id": owner.id,
            "full_name": owner.full_name,
            "father_or_husband_name": owner.father_or_husband_name,
            "address": owner.address,
            "ownership_type": property_owner.ownership_type,
            "ownership_percentage": property_owner.ownership_percentage,
            "created_at": owner.created_at,
        }
        for owner, property_owner in owner_rows
    ]

    total_ownership_percentage = sum(
        owner["ownership_percentage"] or 0
        for owner in owners
    )

    return {
        "id": property_record.id,
        "property_id": property_record.property_id,
        "survey_number": property_record.survey_number,
        "village": property_record.village,
        "tehsil": property_record.tehsil,
        "district": property_record.district,
        "state": property_record.state,
        "area": property_record.area,
        "land_classification": property_record.land_classification,
        "owners": owners,
        "total_ownership_percentage": total_ownership_percentage,
        "created_at": property_record.created_at,
        "updated_at": property_record.updated_at,
    }