
import asyncio
from sqlalchemy import text
from app.database.session import engine


async def test_database():
    try:
        async with engine.connect() as connection:
            result = await connection.execute(text("SELECT 1"))
            print("PostgreSQL connection successful!")
            print("Query result:", result.scalar())
    except Exception as error:
        print("Database connection failed:", error)
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(test_database())
