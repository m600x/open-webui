"""Merge the fork's usage_log chain with the upstream migration head

The fork's usage_log migrations branch off 42e2978c7933, the revision upstream
later built its own 0.11.0 chain on, so the graph carries two heads. config.py
runs command.upgrade(cfg, 'head') — singular — which raises on multiple heads,
so the app would fail to boot at import time without this merge point.

Revision ID: d9e4f7a2c81b
Revises: f2a7c91b4e03, f0bd01a18a3d
Create Date: 2026-07-30 00:00:00.000000

"""

from typing import Sequence, Union

revision: str = 'd9e4f7a2c81b'
down_revision: Union[str, Sequence[str], None] = ('f2a7c91b4e03', 'f0bd01a18a3d')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Topology only — both branches are already applied by the time this runs.
    pass


def downgrade() -> None:
    # Splitting the graph back into two heads is not a data operation.
    pass
