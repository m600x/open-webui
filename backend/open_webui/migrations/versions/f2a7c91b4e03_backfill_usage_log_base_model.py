"""Backfill usage_log.base_model_id from the model table

Revision ID: f2a7c91b4e03
Revises: e91b3d47a2c6
Create Date: 2026-07-14 12:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = 'f2a7c91b4e03'
down_revision: Union[str, None] = 'e91b3d47a2c6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    inspector = sa.inspect(conn)

    tables = inspector.get_table_names()
    if 'usage_log' not in tables or 'model' not in tables:
        return

    # Rows written before base_model_id existed were left NULL, which splits a
    # workspace model's analytics into a NULL-base entry and a current-base
    # entry. Adopt the workspace model's current base for those rows — the
    # best available snapshot for pre-column history.
    op.execute(
        sa.text(
            """
            UPDATE usage_log
            SET base_model_id = (
                SELECT model.base_model_id FROM model WHERE model.id = usage_log.model_id
            )
            WHERE usage_log.base_model_id IS NULL
              AND EXISTS (
                SELECT 1 FROM model
                WHERE model.id = usage_log.model_id
                  AND model.base_model_id IS NOT NULL
                  AND model.base_model_id != usage_log.model_id
              )
            """
        )
    )


def downgrade() -> None:
    # Backfilled rows are indistinguishable from rows recorded at generation
    # time, and write-time snapshots must survive a downgrade; leave data as-is.
    pass
