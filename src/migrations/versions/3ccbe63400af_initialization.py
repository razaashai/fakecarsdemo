"""initialization

Revision ID: 3ccbe63400af
Revises: 
Create Date: 2018-07-12 15:16:01.917908

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ccbe63400af'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('brand',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('manufacturer', sa.String(length=40), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('manufacturer')
    )
    op.create_table('modelcar',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('brand_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=40), nullable=False),
    sa.ForeignKeyConstraint(['brand_id'], ['brand.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('trim',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('model_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=40), nullable=False),
    sa.ForeignKeyConstraint(['model_id'], ['modelcar.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('inventory',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('trim_id', sa.Integer(), nullable=True),
    sa.Column('listed_data', sa.String(length=255), nullable=True),
    sa.Column('ask_price', sa.Integer(), nullable=False),
    sa.Column('condition', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['trim_id'], ['trim.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('inventory')
    op.drop_table('trim')
    op.drop_table('modelcar')
    op.drop_table('brand')
    # ### end Alembic commands ###