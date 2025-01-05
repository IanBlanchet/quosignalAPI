"""ajout de la colonne jours dans la table abonne

Revision ID: 5513cc203d8b
Revises: e987430c6ac0
Create Date: 2025-01-05 09:51:38.885282

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5513cc203d8b'
down_revision: Union[str, None] = 'e987430c6ac0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
