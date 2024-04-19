"""Create Phone Number For User Column

Revision ID: b2bfcb6d83ff
Revises: 
Create Date: 2024-04-19 09:46:49.357037

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b2bfcb6d83ff"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # op.add_column("table_name", sa.Column("new_column", sa.String(255)), nullable=True)
    op.add_column("users", sa.Column("phone_number", sa.String(255), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "phone_number")
