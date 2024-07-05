"""Initial migration

Revision ID: 5e82358bf1eb
Revises: 
Create Date: 2024-07-04 21:32:56.046146

"""
from alembic import op
import sqlalchemy as sa


revision = '5e82358bf1eb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    
    op.create_table('messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(), nullable=True),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    


def downgrade():
    
    op.drop_table('messages')
    