
"""update title relationships

Revision ID: a015e9742233
Revises: 20261114_initial
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a015e9742233"
down_revision: Union[str, Sequence[str], None] = "20261114_initial"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create the many-to-many platform association table.
    op.create_table(
        "title_platforms",
        sa.Column("title_id", sa.Integer(), nullable=False),
        sa.Column("platform_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["title_id"], ["titles.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["platform_id"], ["platforms.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("title_id", "platform_id"),
    )

    # Preserve existing genre assignments.
    op.execute("""
        INSERT INTO title_genres (title_id, genre_id)
        SELECT id, genre_id
        FROM titles
        WHERE genre_id IS NOT NULL
        ON CONFLICT (title_id, genre_id) DO NOTHING
    """)

    # Preserve existing platform assignments.
    op.execute("""
        INSERT INTO title_platforms (title_id, platform_id)
        SELECT id, platform_id
        FROM titles
        WHERE platform_id IS NOT NULL
        ON CONFLICT (title_id, platform_id) DO NOTHING
    """)

    # Update existing genre association foreign keys.
    op.drop_constraint(
        "title_genres_title_id_fkey",
        "title_genres",
        type_="foreignkey",
    )
    op.drop_constraint(
        "title_genres_genre_id_fkey",
        "title_genres",
        type_="foreignkey",
    )

    op.create_foreign_key(
        "title_genres_title_id_fkey",
        "title_genres",
        "titles",
        ["title_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "title_genres_genre_id_fkey",
        "title_genres",
        "genres",
        ["genre_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # Add the missing unique constraint for platform names.
    op.create_unique_constraint(
        "uq_platforms_name",
        "platforms",
        ["name"],
    )

    # Remove old single-relationship foreign keys.
    op.drop_constraint(
        "titles_genre_id_fkey",
        "titles",
        type_="foreignkey",
    )
    op.drop_constraint(
        "titles_platform_id_fkey",
        "titles",
        type_="foreignkey",
    )

    # Remove old columns only after preserving their assignments.
    op.drop_column("titles", "genre_id")
    op.drop_column("titles", "platform_id")


def downgrade() -> None:
    # Restore the old single-relationship columns.
    op.add_column(
        "titles",
        sa.Column("genre_id", sa.Integer(), nullable=True),
    )
    op.add_column(
        "titles",
        sa.Column("platform_id", sa.Integer(), nullable=True),
    )

    op.create_foreign_key(
        "titles_genre_id_fkey",
        "titles",
        "genres",
        ["genre_id"],
        ["id"],
    )
    op.create_foreign_key(
        "titles_platform_id_fkey",
        "titles",
        "platforms",
        ["platform_id"],
        ["id"],
    )

    # Restore one relationship per title.
    # If multiple relationships exist, the lowest ID is selected.
    op.execute("""
        UPDATE titles
        SET genre_id = (
            SELECT MIN(genre_id)
            FROM title_genres
            WHERE title_genres.title_id = titles.id
        )
    """)

    op.execute("""
        UPDATE titles
        SET platform_id = (
            SELECT MIN(platform_id)
            FROM title_platforms
            WHERE title_platforms.title_id = titles.id
        )
    """)

    # Restore the original genre foreign keys.
    op.drop_constraint(
        "title_genres_title_id_fkey",
        "title_genres",
        type_="foreignkey",
    )
    op.drop_constraint(
        "title_genres_genre_id_fkey",
        "title_genres",
        type_="foreignkey",
    )

    op.create_foreign_key(
        "title_genres_title_id_fkey",
        "title_genres",
        "titles",
        ["title_id"],
        ["id"],
    )
    op.create_foreign_key(
        "title_genres_genre_id_fkey",
        "title_genres",
        "genres",
        ["genre_id"],
        ["id"],
    )

    op.drop_table("title_platforms")

    op.drop_constraint(
        "uq_platforms_name",
        "platforms",
        type_="unique",
    )
