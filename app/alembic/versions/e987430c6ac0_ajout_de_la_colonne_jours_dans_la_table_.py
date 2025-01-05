"""ajout de la colonne jours dans la table abonne

Revision ID: e987430c6ac0
Revises: b1951b9cb88f
Create Date: 2025-01-05 09:49:25.189697

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e987430c6ac0'
down_revision: Union[str, None] = 'b1951b9cb88f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
