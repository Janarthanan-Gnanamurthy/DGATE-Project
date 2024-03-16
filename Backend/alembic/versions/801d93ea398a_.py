"""empty message

Revision ID: 801d93ea398a
Revises: ccb668e34153
Create Date: 2024-03-06 22:16:37.057075

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '801d93ea398a'
down_revision: Union[str, None] = 'ccb668e34153'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('questions', 'answer_uri',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_constraint('questions_option_a_key', 'questions', type_='unique')
    op.drop_constraint('questions_option_b_key', 'questions', type_='unique')
    op.drop_constraint('questions_option_c_key', 'questions', type_='unique')
    op.drop_constraint('questions_option_d_key', 'questions', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('questions_option_d_key', 'questions', ['option_d'])
    op.create_unique_constraint('questions_option_c_key', 'questions', ['option_c'])
    op.create_unique_constraint('questions_option_b_key', 'questions', ['option_b'])
    op.create_unique_constraint('questions_option_a_key', 'questions', ['option_a'])
    op.alter_column('questions', 'answer_uri',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
