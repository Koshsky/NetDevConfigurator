"""Add name field to presets table

Revision ID: 78e3c6bfb2d5
Revises: be2683b91e98
Create Date: 2025-03-17 21:16:15.428466

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "78e3c6bfb2d5"
down_revision: Union[str, None] = "be2683b91e98"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Добавляем поле name
    op.add_column("presets", sa.Column("name", sa.String(256), nullable=True))

    # Копируем значения из role в name
    op.execute("UPDATE presets SET name = role")

    # Делаем поле name NOT NULL
    op.alter_column("presets", "name", existing_type=sa.String(256), nullable=False)

    # Создаем функцию триггера
    op.execute("""
        CREATE OR REPLACE FUNCTION update_preset_name()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.name = NEW.role;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    # Создаем триггер
    op.execute("""
        CREATE TRIGGER update_preset_name_trigger
        BEFORE INSERT OR UPDATE ON presets
        FOR EACH ROW
        EXECUTE FUNCTION update_preset_name();
    """)


def downgrade() -> None:
    # Удаляем триггер
    op.execute("DROP TRIGGER IF EXISTS update_preset_name_trigger ON presets")

    # Удаляем функцию триггера
    op.execute("DROP FUNCTION IF EXISTS update_preset_name()")

    # Удаляем поле name
    op.drop_column("presets", "name")
