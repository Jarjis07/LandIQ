"""add authentication fields

Revision ID: 1f877be53b35
Revises:
Create Date: 2026-09-13 15:07:16.359097

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "1f877be53b35"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade users table for authentication and RBAC."""

    # Add authentication fields.
    op.add_column(
        "users",
        sa.Column(
            "password_hash",
            sa.String(length=255),
            nullable=False,
        ),
    )

    op.add_column(
        "users",
        sa.Column(
            "role_id",
            sa.Integer(),
            nullable=False,
        ),
    )

    op.add_column(
        "users",
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
        ),
    )

    # Create default application roles.
    op.execute(
    """
    INSERT INTO roles (
        name,
        description,
        is_active,
        created_at
    )
    VALUES
        (
            'admin',
            'System administrator',
            TRUE,
            CURRENT_TIMESTAMP
        ),
        (
            'land_officer',
            'Land officer',
            TRUE,
            CURRENT_TIMESTAMP
        ),
        (
            'verifier',
            'Land record verifier',
            TRUE,
            CURRENT_TIMESTAMP
        ),
        (
            'citizen',
            'Citizen or general user',
            TRUE,
            CURRENT_TIMESTAMP
        )
    """
    )

    # Add RBAC index.
    op.create_index(
        "ix_users_role_id",
        "users",
        ["role_id"],
        unique=False,
    )

    # Add named foreign key.
    op.create_foreign_key(
        "fk_users_role_id_roles",
        "users",
        "roles",
        ["role_id"],
        ["id"],
    )

    # Remove old denormalized role field.
    op.drop_column(
        "users",
        "role",
    )


def downgrade() -> None:
    """Revert authentication and RBAC changes."""

    # Restore old role column.
    op.add_column(
        "users",
        sa.Column(
            "role",
            sa.String(length=50),
            nullable=True,
        ),
    )

    # Restore role names from normalized role records.
    op.execute(
        """
        UPDATE users
        SET role = roles.name
        FROM roles
        WHERE users.role_id = roles.id
        """
    )

    op.execute(
        """
        UPDATE users
        SET role = 'verifier'
        WHERE role IS NULL
        """
    )

    op.alter_column(
        "users",
        "role",
        existing_type=sa.String(length=50),
        nullable=False,
    )

    # Remove foreign key and index.
    op.drop_constraint(
        "fk_users_role_id_roles",
        "users",
        type_="foreignkey",
    )

    op.drop_index(
        "ix_users_role_id",
        table_name="users",
    )

    # Remove authentication fields.
    op.drop_column(
        "users",
        "updated_at",
    )

    op.drop_column(
        "users",
        "role_id",
    )

    op.drop_column(
        "users",
        "password_hash",
    )