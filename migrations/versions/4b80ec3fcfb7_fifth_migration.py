"""fifth migration

Revision ID: 4b80ec3fcfb7
Revises: 7edeef2ab637
Create Date: 2020-05-13 20:50:49.110458

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b80ec3fcfb7'
down_revision = '7edeef2ab637'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('subscribers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('pass_secure', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_subscribers_email'), 'subscribers', ['email'], unique=True)
    op.create_index(op.f('ix_subscribers_username'), 'subscribers', ['username'], unique=False)
    op.drop_constraint('reviews_user_id_fkey', 'reviews', type_='foreignkey')
    op.drop_column('reviews', 'user_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reviews', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('reviews_user_id_fkey', 'reviews', 'users', ['user_id'], ['id'])
    op.drop_index(op.f('ix_subscribers_username'), table_name='subscribers')
    op.drop_index(op.f('ix_subscribers_email'), table_name='subscribers')
    op.drop_table('subscribers')
    # ### end Alembic commands ###
