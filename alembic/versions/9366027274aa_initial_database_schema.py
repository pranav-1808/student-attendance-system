"""Initial database schema

Revision ID: 9366027274aa
Revises:
Create Date: 2026-10-01 13:08:37.689844

"""

from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "9366027274aa"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""


def downgrade() -> None:
    """Downgrade schema."""
