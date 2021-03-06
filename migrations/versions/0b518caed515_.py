"""empty message

Revision ID: 0b518caed515
Revises: d12994d5be66
Create Date: 2018-04-18 23:30:57.896096

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b518caed515'
down_revision = 'd12994d5be66'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tracks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('artist', sa.String(length=140), nullable=True),
    sa.Column('album', sa.String(length=140), nullable=True),
    sa.Column('track', sa.String(length=140), nullable=True),
    sa.Column('filelocation', sa.String(length=140), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('requests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('track_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['track_id'], ['tracks.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_requests_timestamp'), 'requests', ['timestamp'], unique=False)
    op.drop_index('ix_request_log_timestamp', table_name='request_log')
    op.drop_table('request_log')
    op.drop_table('track_library')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('track_library',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('artist', sa.VARCHAR(length=140), nullable=True),
    sa.Column('album', sa.VARCHAR(length=140), nullable=True),
    sa.Column('track', sa.VARCHAR(length=140), nullable=True),
    sa.Column('filelocation', sa.VARCHAR(length=140), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('request_log',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('timestamp', sa.DATETIME(), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_request_log_timestamp', 'request_log', ['timestamp'], unique=False)
    op.drop_index(op.f('ix_requests_timestamp'), table_name='requests')
    op.drop_table('requests')
    op.drop_table('tracks')
    # ### end Alembic commands ###
