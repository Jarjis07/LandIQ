from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.role import Role
from app.models.user import User


def authenticate_user(
    db: Session,
    email: str,
    password: str,
) -> User | None:
    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if user is None:
        return None

    if not user.is_active:
        return None

    if not verify_password(
        password,
        user.password_hash,
    ):
        return None

    return user


def create_user(
    db: Session,
    name: str,
    email: str,
    password: str,
    role_name: str,
) -> User:
    existing_user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if existing_user:
        raise ValueError("User with this email already exists")

    role = (
        db.query(Role)
        .filter(Role.name == role_name)
        .first()
    )

    if role is None:
        raise ValueError(
            f"Role '{role_name}' does not exist"
        )

    user = User(
        name=name,
        email=email,
        password_hash=hash_password(password),
        role_id=role.id,
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def generate_login_token(user: User) -> str:
    return create_access_token(
        {
            "sub": str(user.id),
            "role_id": user.role_id,
        }
    )