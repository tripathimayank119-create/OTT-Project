import asyncio
import pytest
from typing import Generator
from httpx import AsyncClient, ASGITransport

from app.main import app


@pytest.fixture(scope="session")
def test_app() -> Generator:
    """Create test FastAPI application."""
    yield app


@pytest.fixture(scope="session")
def client(test_app) -> Generator:
    """Create test client."""
    transport = ASGITransport(app=test_app)
    client = AsyncClient(transport=transport, base_url="http://test")
    yield client
    asyncio.run(client.aclose())


@pytest.fixture
def superuser_credentials():
    """Superuser test credentials."""
    return {"email": "admin@example.com", "password": "adminpassword123"}


@pytest.fixture
def regular_user_credentials():
    """Regular user test credentials."""
    return {"email": "user@example.com", "password": "userpassword123"}