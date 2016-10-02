"""Add ImageMatchRequest table

Revision ID: 66d446c182a5
Revises: de0968aefcb0
Create Date: 2016-10-08 15:14:56.686056

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '66d446c182a5'
down_revision = 'de0968aefcb0'
branch_labels = None
depends_on = None

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('image_match_requests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('image_s3_url', sa.String(), nullable=True),
    sa.Column('short_code', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_column(u'image_derivatives', 'image_path')
    op.drop_column(u'item_images', 'image_path')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column(u'item_images', sa.Column('image_path', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column(u'image_derivatives', sa.Column('image_path', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_table('image_match_requests')
    ### end Alembic commands ###