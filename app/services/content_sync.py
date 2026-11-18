
from typing import Any, Dict, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.title import Title, Genre, Platform
from app.core.cache import cache_clear


async def sync_catalogue(
    catalogue_data: List[Dict[str, Any]],
    session: AsyncSession,
) -> Dict[str, Any]:

    added = 0
    updated = 0
    skipped = 0

    try:
        for item in catalogue_data:

            title_name = item.get("title")

            if not title_name:
                skipped += 1
                continue

            result = await session.execute(
                select(Title).where(
                    Title.title == title_name
                )
            )

            title = result.scalar_one_or_none()

            genre_objects = []

            for genre_name in item.get("genres", []):
                genre_result = await session.execute(
                    select(Genre).where(
                        Genre.name.ilike(genre_name)
                    )
                )

                genre = genre_result.scalar_one_or_none()

                if genre is None:
                    genre = Genre(name=genre_name)
                    session.add(genre)
                    await session.flush()

                genre_objects.append(genre)

            platform_objects = []

            for platform_name in item.get("platforms", []):
                slug = platform_name.lower().replace(" ", "-")

                platform_result = await session.execute(
                    select(Platform).where(
                        Platform.slug == slug
                    )
                )

                platform = platform_result.scalar_one_or_none()

                if platform is None:
                    platform = Platform(
                        name=platform_name,
                        slug=slug,
                    )

                    session.add(platform)
                    await session.flush()

                platform_objects.append(platform)

            title_fields = {
                "original_title": item.get("original_title"),
                "description": item.get("description"),
                "release_year": item.get("release_year"),
                "rating": item.get("rating"),
                "duration_minutes": item.get("duration_minutes"),
                "is_featured": item.get("is_featured", False),
            }

            if title is None:
                title = Title(
                    title=title_name,
                    **title_fields,
                    genres=genre_objects,
                    platforms=platform_objects,
                )

                session.add(title)
                added += 1

            else:
                for field, value in title_fields.items():
                    setattr(title, field, value)

                title.genres = genre_objects
                title.platforms = platform_objects

                updated += 1

        await session.commit()

        await cache_clear()

        return {
            "status": "success",
            "message": "Catalogue synchronization completed",
            "total_processed": len(catalogue_data),
            "added": added,
            "updated": updated,
            "skipped": skipped,
        }

    except Exception as error:
        await session.rollback()

        return {
            "status": "failed",
            "message": "Catalogue synchronization failed",
            "error": str(error),
            "total_processed": len(catalogue_data),
            "added": 0,
            "updated": 0,
            "skipped": skipped,
        }
