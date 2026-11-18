
"""Initial database migration.

Revision ID: 20261114_initial
Revises:
Create Date: 2026-11-14 00:00:00
"""

from alembic import op
import sqlalchemy as sa


# Revision identifiers
revision = "20261114_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create the initial database tables."""

    # Users table
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_superuser", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email", name="uix_email"),
    )

    # Genres table
    op.create_table(
        "genres",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name", name="ix_genres_name"),
    )

    # Platforms table
    op.create_table(
        "platforms",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("slug", sa.String(100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slug", name="ix_platforms_slug"),
    )

    # Titles table
    op.create_table(
        "titles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("original_title", sa.String(255), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("release_year", sa.Integer(), nullable=True),
        sa.Column("rating", sa.Float(), nullable=True),
        sa.Column("duration_minutes", sa.Integer(), nullable=True),
        sa.Column("is_featured", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("genre_id", sa.Integer(), nullable=True),
        sa.Column("platform_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["genre_id"], ["genres.id"]),
        sa.ForeignKeyConstraint(["platform_id"], ["platforms.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    # Title indexes
    op.create_index(
        "ix_titles_title",
        "titles",
        ["title"],
        unique=False,
    )

    op.create_index(
        "ix_titles_release_year",
        "titles",
        ["release_year"],
        unique=False,
    )

    op.create_index(
        "ix_titles_is_featured",
        "titles",
        ["is_featured"],
        unique=False,
    )

    # Title-genre association table
    op.create_table(
        "title_genres",
        sa.Column("title_id", sa.Integer(), nullable=False),
        sa.Column("genre_id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("title_id", "genre_id"),
        sa.ForeignKeyConstraint(["title_id"], ["titles.id"]),
        sa.ForeignKeyConstraint(["genre_id"], ["genres.id"]),
    )


def downgrade() -> None:
    """Remove the initial database tables."""

    op.drop_table("title_genres")

    op.drop_index(
        "ix_titles_is_featured",
        table_name="titles",
    )

    op.drop_index(
        "ix_titles_release_year",
        table_name="titles",
    )

    op.drop_index(
        "ix_titles_title",
        table_name="titles",
    )

    op.drop_table("titles")
    op.drop_table("platforms")
    op.drop_table("genres")
    op.drop_table("users")
