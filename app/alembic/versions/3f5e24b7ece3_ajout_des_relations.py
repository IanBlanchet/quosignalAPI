"""ajout des relations

Revision ID: 3f5e24b7ece3
Revises: 8e1d3cf04c7d
Create Date: 2024-12-24 13:43:38.230031

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3f5e24b7ece3'
down_revision: Union[str, None] = '8e1d3cf04c7d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
