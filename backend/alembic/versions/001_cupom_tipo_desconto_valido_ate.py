"""cupom: tipo_desconto, desconto_fixo, valido_ate, usos nullable

Revision ID: 001
Revises:
Create Date: 2026-06-13
"""
from alembic import op
import sqlalchemy as sa

revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("cupons", schema=None) as batch_op:
        batch_op.add_column(sa.Column("tipo_desconto", sa.String(10), nullable=False, server_default="percentual"))
        batch_op.add_column(sa.Column("desconto_fixo", sa.Numeric(10, 2), nullable=True))
        batch_op.add_column(sa.Column("valido_ate", sa.Date(), nullable=True))
        batch_op.alter_column("usos_maximos", existing_type=sa.Integer(), nullable=True)
        batch_op.alter_column("usos_restantes", existing_type=sa.Integer(), nullable=True)
        batch_op.create_check_constraint(
            "ck_cupons_tipo_desconto",
            "tipo_desconto IN ('percentual', 'fixo')",
        )


def downgrade() -> None:
    with op.batch_alter_table("cupons", schema=None) as batch_op:
        batch_op.drop_constraint("ck_cupons_tipo_desconto", type_="check")
        batch_op.alter_column("usos_maximos", existing_type=sa.Integer(), nullable=False)
        batch_op.alter_column("usos_restantes", existing_type=sa.Integer(), nullable=False)
        batch_op.drop_column("valido_ate")
        batch_op.drop_column("desconto_fixo")
        batch_op.drop_column("tipo_desconto")
