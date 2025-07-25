"""Add assigned_to to Incident

Revision ID: 0a93556466ff
Revises: 036e75072582
Create Date: 2025-07-19 12:55:14.826850

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a93556466ff'
down_revision = '036e75072582'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('incident', schema=None) as batch_op:
        batch_op.add_column(sa.Column('assigned_to_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_incident_user', 'user', ['assigned_to_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('incident', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('assigned_to_id')

    # ### end Alembic commands ###
