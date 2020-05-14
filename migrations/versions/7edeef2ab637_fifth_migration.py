"""fifth migration

Revision ID: 7edeef2ab637
Revises: 5595ad14bcf5
Create Date: 2020-05-13 05:14:43.748249

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7edeef2ab637'
down_revision = '5595ad14bcf5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_blogposts_quote', table_name='blogposts')
    op.drop_index('ix_blogposts_user_id', table_name='blogposts')
    op.drop_index('ix_profile_photos_user_id', table_name='profile_photos')
    op.drop_index('ix_reviews_user_id', table_name='reviews')
    op.create_foreign_key(None, 'reviews', 'blogposts', ['quote_id'], ['id'])
    op.drop_column('reviews', 'quote')
    op.drop_column('reviews', 'author')
    op.drop_index('ix_users_role_id', table_name='users')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_users_role_id', 'users', ['role_id'], unique=False)
    op.add_column('reviews', sa.Column('author', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('reviews', sa.Column('quote', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'reviews', type_='foreignkey')
    op.create_index('ix_reviews_user_id', 'reviews', ['user_id'], unique=False)
    op.create_index('ix_profile_photos_user_id', 'profile_photos', ['user_id'], unique=False)
    op.create_index('ix_blogposts_user_id', 'blogposts', ['user_id'], unique=False)
    op.create_index('ix_blogposts_quote', 'blogposts', ['quote'], unique=False)
    # ### end Alembic commands ###
