"""Adicionando atributos de usuarios

Revision ID: c8a4261a85a1
Revises: 3998a560515e
Create Date: 2021-06-10 08:35:53.653653

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c8a4261a85a1'
down_revision = '3998a560515e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('name', sa.String(length=64), nullable=True))
    op.add_column('users', sa.Column('location', sa.String(length=64), nullable=True))
    op.add_column('users', sa.Column('about_me', sa.Text(), nullable=True))
    op.add_column('users', sa.Column('member_since', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('last_seen', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'last_seen')
    op.drop_column('users', 'member_since')
    op.drop_column('users', 'about_me')
    op.drop_column('users', 'location')
    op.drop_column('users', 'name')
    # ### end Alembic commands ###
