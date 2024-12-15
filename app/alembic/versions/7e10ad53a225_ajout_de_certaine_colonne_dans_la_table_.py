"""ajout de certaine colonne dans la table abonne

Revision ID: 7e10ad53a225
Revises: 
Create Date: 2024-12-15 13:29:58.907843

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7e10ad53a225'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
