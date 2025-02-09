"""deplacer la colonne lien dans la table dassociation

Revision ID: b1951b9cb88f
Revises: 544db7e41d12
Create Date: 2024-12-29 16:39:35.512370

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b1951b9cb88f'
down_revision: Union[str, None] = '544db7e41d12'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ass_abonne_contactUrgence', sa.Column('lien', sa.String(length=30), nullable=True))
    op.drop_column('contactUrgence', 'lien')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contactUrgence', sa.Column('lien', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
    op.drop_column('ass_abonne_contactUrgence', 'lien')
    # ### end Alembic commands ###
