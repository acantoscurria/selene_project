"""cambios menores

Revision ID: 15fe943b2331
Revises: caa0bb35fbe6
Create Date: 2024-04-15 08:54:57.191910

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from alembic_postgresql_enum import TableReference

# revision identifiers, used by Alembic.
revision: str = '15fe943b2331'
down_revision: Union[str, None] = 'caa0bb35fbe6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('invites', 'otp_code')
    op.drop_column('invites', 'otp_expired')
    op.sync_enum_values('public', 'gender', ['Masculino', 'Femenino', 'Otros'],
                        [TableReference(table_schema='public', table_name='invites', column_name='gender')],
                        enum_values_to_rename=[])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.sync_enum_values('public', 'gender', ['MALE', 'FEMALE'],
                        [TableReference(table_schema='public', table_name='invites', column_name='gender')],
                        enum_values_to_rename=[])
    op.add_column('invites', sa.Column('otp_expired', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('invites', sa.Column('otp_code', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###