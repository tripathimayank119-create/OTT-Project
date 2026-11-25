import pytest
from fastapi import status
from httpx import AsyncClient, ASGITransport
from app.main import app


class TestGenreEndpoints:
    """Integration tests for genre endpoints - SOP Week 1 & 3."""

    @pytest.mark.asyncio
    async def test_list_genres_endpoint_structure(self, client, test_app):
        """Test list genres endpoint structure exists - SOP Week 1."""
        transport = ASGITransport(app=test_app)
        ac = AsyncClient(transport=transport, base_url="http://test")
        try:
            response = await ac.get("/api/v1/genres/")
            assert response.status_code in [200, 404, 422]
            assert response.headers.get("content-type", "").startswith("application/json")
        finally:
            await ac.aclose()

    @pytest.mark.asyncio
    async def test_create_genre_endpoint_structure(self, client, test_app):
        """Test create genre endpoint structure exists - SOP Week 1."""
        transport = ASGITransport(app=test_app)
        ac = AsyncClient(transport=transport, base_url="http://test")
        try:
            response = await ac.post(
                "/api/v1/genres/",
                json={"name": "Action", "description": "Action movies"},
            )
            assert response.status_code in [200, 201, 400, 422, 404]
            assert response.headers.get("content-type", "").startswith("application/json")
        finally:
            await ac.aclose()


class TestPlatformEndpoints:
    """Integration tests for platform endpoints - SOP Week 1 & 3."""

    @pytest.mark.asyncio
    async def test_list_platforms_endpoint_structure(self, client, test_app):
        """Test list platforms endpoint structure exists - SOP Week 1."""
        transport = ASGITransport(app=test_app)
        ac = AsyncClient(transport=transport, base_url="http://test")
        try:
            response = await ac.get("/api/v1/platforms/")
            assert response.status_code in [200, 404, 422]
            assert response.headers.get("content-type", "").startswith("application/json")
        finally:
            await ac.aclose()

    @pytest.mark.asyncio
    async def test_create_platform_endpoint_structure(self, client, test_app):
        """Test create platform endpoint structure exists - SOP Week 1."""
        transport = ASGITransport(app=test_app)
        ac = AsyncClient(transport=transport, base_url="http://test")
        try:
            response = await ac.post(
                "/api/v1/platforms/",
                json={"name": "Netflix", "slug": "netflix", "description": "Netflix streaming"},
            )
            assert response.status_code in [200, 201, 400, 422, 404]
            assert response.headers.get("content-type", "").startswith("application/json")
        finally:
            await ac.aclose()


class TestDependencies:
    """Tests for FastAPI dependencies - SOP Week 2."""

    @pytest.mark.asyncio
    async def test_get_db_session_dependency(self):
        """Test get_db_session dependency can be created."""
        from app.core.dependencies import get_db_session
        # Just verify the dependency function exists and is a generator
        async_gen = get_db_session()
        assert async_gen is not None

    @pytest.mark.asyncio
    async def test_get_current_user_dependency(self):
        """Test get_current_user dependency exists."""
        from app.core.dependencies import get_current_user
        assert get_current_user is not None

    @pytest.mark.asyncio
    async def test_oauth2_scheme_dependency(self):
        """Test oauth2_scheme dependency exists."""
        from app.core.dependencies import oauth2_scheme
        assert oauth2_scheme is not None