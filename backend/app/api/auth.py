from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth_service import (
    authenticate_user,
    generate_login_token,
)
from app.models.user import User
from app.core.dependencies import get_current_user, require_roles

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    user = authenticate_user(
        db=db,
        email=request.email,
        password=request.password,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = generate_login_token(user)

    return TokenResponse(
        access_token=token,
    )

@router.get("/me")
def get_my_profile(
    current_user: User = Depends(get_current_user),
):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role_id": current_user.role_id,
        "is_active": current_user.is_active,
    }

@router.get("/admin-test")
def admin_test(
    current_user: User = Depends(
        require_roles("admin")
    ),
):
    return {
        "message": "Admin access granted",
        "user_id": current_user.id,
        "email": current_user.email,
    }