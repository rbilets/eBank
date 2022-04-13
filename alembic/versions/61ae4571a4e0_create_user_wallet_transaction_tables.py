"""Create user, wallet, transaction tables

Revision ID: 61ae4571a4e0
Revises: 
Create Date: 2021-10-27 15:09:36.030236

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61ae4571a4e0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('uid', sa.String(), primary_key=True),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('username', sa.String(), nullable=False, unique=True),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('first_name', sa.String(), nullable=False),
        sa.Column('last_name', sa.String(), nullable=False),
        sa.Column('is_admin', sa.Boolean, nullable=False, default=False)
    )

    op.create_table(
        'wallets',
        sa.Column('uid', sa.String(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('funds', sa.Float, nullable=False),
        sa.Column('owner_id', sa.String, sa.ForeignKey('users.uid'))
    )

    op.create_table(
        'transactions',
        sa.Column('uid', sa.Integer, primary_key=True),
        sa.Column('from_wallet_id', sa.String(), sa.ForeignKey('wallets.uid')),
        sa.Column('to_wallet_id', sa.String(), sa.ForeignKey('wallets.uid')),
        sa.Column('amount', sa.Float, nullable=False),
        sa.Column('status', sa.Boolean, nullable=False)
    )


def downgrade():
    op.drop_table('users')
    op.drop_table('wallets')
    op.drop_table('transactions')
