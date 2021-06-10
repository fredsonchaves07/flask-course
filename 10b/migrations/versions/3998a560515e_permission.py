"""permission

Revision ID: 3998a560515e
Revises: cc2233f4bcc4
Create Date: 2021-06-09 09:26:07.755678

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3998a560515e'
down_revision = 'cc2233f4bcc4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('roles', sa.Column('default', sa.Boolean(), nullable=True))
    op.add_column('roles', sa.Column('permissions', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_roles_default'), 'roles', ['default'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_roles_default'), table_name='roles')
    op.drop_column('roles', 'permissions')
    op.drop_column('roles', 'default')
    # ### end Alembic commands ###
