"""add users updated at

Revision ID: 29db16702588
Revises: 1f877be53b35
Create Date: 2026-09-13

"""

from typing import Sequence, Union

from alembic import op


revision: str = "29db16702588"
down_revision: Union[str, Sequence[str], None] = "1f877be53b35"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Mark users.updated_at as present in the database."""
    pass


def downgrade() -> None:
    """No database change is required."""
    pass