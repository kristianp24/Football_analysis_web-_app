"""Modified token column

Revision ID: abd0b32d3241
Revises: aeba1da9f995
Create Date: 2025-03-14 13:00:17.541750

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'abd0b32d3241'
down_revision = 'aeba1da9f995'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('token', new_column_name='token', existing_type=mysql.VARCHAR(length=200), nullable=True, new_type=mysql.VARCHAR(length=600))
    

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('full_name', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('email', mysql.VARCHAR(length=100), nullable=False),
    sa.Column('hashed_password', mysql.VARCHAR(length=200), nullable=False),
    sa.Column('token', mysql.VARCHAR(length=200), nullable=True),
    sa.Column('token_expiration', mysql.DATETIME(), nullable=True),
    sa.Column('created_at', mysql.DATETIME(), nullable=True),
    sa.Column('updated_at', mysql.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mariadb_collate='latin1_swedish_ci',
    mariadb_default_charset='latin1',
    mariadb_engine='InnoDB'
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_index('email', ['email'], unique=True)

    op.create_table('videos',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('video', sa.BLOB(), nullable=True),
    sa.Column('user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='videos_ibfk_1', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    mariadb_collate='latin1_swedish_ci',
    mariadb_default_charset='latin1',
    mariadb_engine='InnoDB'
    )
    with op.batch_alter_table('videos', schema=None) as batch_op:
        batch_op.create_index('ix_videos_user_id', ['user_id'], unique=False)

    # ### end Alembic commands ###
