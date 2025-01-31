"""Add tabela Veiculo nome campo abservacao .

Revision ID: d5865bbab1cb
Revises: 76f23e70bce1
Create Date: 2025-01-26 20:45:36.534724

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd5865bbab1cb'
down_revision = '76f23e70bce1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('veiculo', schema=None) as batch_op:
        batch_op.add_column(sa.Column('observacao_carro', sa.String(length=255), nullable=True))
        batch_op.drop_column('observacao_Carro')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('veiculo', schema=None) as batch_op:
        batch_op.add_column(sa.Column('observacao_Carro', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
        batch_op.drop_column('observacao_carro')

    # ### end Alembic commands ###
