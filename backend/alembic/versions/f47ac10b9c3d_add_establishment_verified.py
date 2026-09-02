"""add establishment verified column

Revision ID: f47ac10b9c3d
Revises:  (baseline — prior alembic history was lost; versions/ was empty)
Create Date: 2026-08-20

Adds the `verified` boolean column to ESTABLISHMENT so the business
verification flow (/api/business/verification, /api/admin/merchants/{id}/verify)
can persist approval state. Idempotent: skips if the column already exists.
"""
import sqlalchemy as sa
from alembic import op

revision = "f47ac10b9c3d"
down_revision = None
branch_labels = None
depends_on = None


def _has_column(table: str, column: str) -> bool:
    bind = op.get_bind()
    rows = bind.execute(sa.text(f"PRAGMA table_info({table})")).fetchall()
    return any(r[1] == column for r in rows)


def upgrade() -> None:
    if not _has_column("ESTABLISHMENT", "verified"):
        op.add_column(
            "ESTABLISHMENT",
            sa.Column("verified", sa.Boolean(), server_default=sa.false(), nullable=False),
        )


def downgrade() -> None:
    if _has_column("ESTABLISHMENT", "verified"):
        op.drop_column("ESTABLISHMENT", "verified")
