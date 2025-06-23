"""edit icons field

Revision ID: eb34f1097cca
Revises: e888d825c96e
Create Date: 2025-06-23 11:11:38.089793

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = 'eb34f1097cca'
down_revision: Union[str, None] = 'e888d825c96e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('ftks', sa.Column('icons_json', postgresql.JSON(astext_type=sa.Text())))

    conn = op.get_bind()
    conn.execute(text("""
        UPDATE ftks 
        SET icons_json = jsonb_build_object('legacy_data', icons)
        WHERE icons IS NOT NULL
    """))

    op.drop_column('ftks', 'icons')

    op.alter_column('ftks', 'icons_json', new_column_name='icons')


def downgrade() -> None:
    op.add_column('ftks', sa.Column('icons_array', postgresql.ARRAY(sa.VARCHAR())))

    conn = op.get_bind()
    conn.execute(text("""
        UPDATE ftks 
        SET icons_array = CASE 
            WHEN icons->'legacy_data' IS NOT NULL THEN (icons->'legacy_data')::text[]::varchar[]
            ELSE '{}'::varchar[]
        END
    """))

    op.drop_column('ftks', 'icons')

    op.alter_column('ftks', 'icons_array', new_column_name='icons')