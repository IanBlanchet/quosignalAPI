"""ajout des relations

Revision ID: a313adef97d1
Revises: 3f5e24b7ece3
Create Date: 2024-12-24 13:50:24.405170

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a313adef97d1'
down_revision: Union[str, None] = '3f5e24b7ece3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
