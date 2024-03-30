"""dni unique

Revision ID: a0e79e95159a
Revises: 2cfd125b4fd0
Create Date: 2024-03-29 20:31:11.898654

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'a0e79e95159a'
down_revision: Union[str, None] = '2cfd125b4fd0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'invites', ['dni'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'invites', type_='unique')
    # ### end Alembic commands ###