"""ajout relation many to many entre abonne et contact urgence

Revision ID: fdcf8f5387b0
Revises: 9d1100800330
Create Date: 2024-12-29 11:15:13.727981

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fdcf8f5387b0'
down_revision: Union[str, None] = '9d1100800330'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###