"""add_character_updated_at_and_token_hash

Revision ID: c2d3e4f5a6b7
Revises: 9b844eab8995
Create Date: 2026-07-10 12:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c2d3e4f5a6b7'
down_revision: Union[str, None] = '9b844eab8995'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1) Agregar updated_at a characters
    op.add_column('characters', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))

    # 2) Migrar reset_tokens: token -> token_hash
    #    Primero crear la nueva columna
    op.add_column('reset_tokens', sa.Column('token_hash', sa.String(length=64), nullable=True))

    #    Copiar datos existentes (token ya contiene hashes bcrypt, los convertimos a SHA-256 no es posible
    #    retroactivamente, así que limpiamos tokens viejos que ya no servirían con el nuevo esquema)
    op.execute("DELETE FROM reset_tokens")

    #    Ahora hacer NOT NULL y agregar índice único
    op.alter_column('reset_tokens', 'token_hash', nullable=False)
    op.create_unique_index('uq_reset_tokens_token_hash', 'reset_tokens', ['token_hash'])
    op.create_index('ix_reset_tokens_token_hash', 'reset_tokens', ['token_hash'])

    #    Eliminar columna vieja e índice viejo
    op.drop_index('ix_reset_tokens_token', table_name='reset_tokens')
    op.drop_column('reset_tokens', 'token')


def downgrade() -> None:
    # Revertir cambios
    op.add_column('reset_tokens', sa.Column('token', sa.String(length=255), nullable=True))
    op.execute("DELETE FROM reset_tokens")
    op.alter_column('reset_tokens', 'token', nullable=False)
    op.create_index('ix_reset_tokens_token', 'reset_tokens', ['token'], unique=False)
    op.drop_index('ix_reset_tokens_token_hash', table_name='reset_tokens')
    op.drop_index('uq_reset_tokens_token_hash', table_name='reset_tokens')
    op.drop_column('reset_tokens', 'token_hash')
    op.drop_column('characters', 'updated_at')
