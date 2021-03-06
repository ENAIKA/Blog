"""second migration

Revision ID: b1aa54ade1f0
Revises: 6a258b4b1ee8
Create Date: 2020-05-11 15:37:21.353855

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1aa54ade1f0'
down_revision = '6a258b4b1ee8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('secondblogs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('blogTitle', sa.String(length=255), nullable=True),
    sa.Column('blogPost', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_secondblogs_blogPost'), 'secondblogs', ['blogPost'], unique=False)
    op.create_index(op.f('ix_secondblogs_user_id'), 'secondblogs', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_secondblogs_user_id'), table_name='secondblogs')
    op.drop_index(op.f('ix_secondblogs_blogPost'), table_name='secondblogs')
    op.drop_table('secondblogs')
    # ### end Alembic commands ###
