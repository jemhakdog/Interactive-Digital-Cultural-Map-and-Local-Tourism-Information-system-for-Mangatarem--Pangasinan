"""add reset_token columns to USER table

Revision ID: f1a2b3c4d5e6
Revises: ce17e243724a
Create Date: 2026-08-18
"""
from alembic import op
import sqlalchemy as sa

revision = 'f1a2b3c4d5e6'
down_revision = 'ce17e243724a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('USER', sa.Column('reset_token', sa.String(128), nullable=True, unique=True))
    op.add_column('USER', sa.Column('reset_token_expires_at', sa.DateTime(), nullable=True))
    op.add_column('USER', sa.Column('reset_token_used', sa.Boolean(), nullable=True, default=False))


def downgrade():
    op.drop_column('USER', 'reset_token_used')
    op.drop_column('USER', 'reset_token_expires_at')
    op.drop_column('USER', 'reset_token')
