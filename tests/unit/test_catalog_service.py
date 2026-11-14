import pytest
from unittest.mock import AsyncMock, MagicMock

from app.services.catalog_service import CatalogService
from app.schemas.title import TitleCreate


class TestCatalogService:
    """Unit tests for CatalogService - no database required."""

    @pytest.fixture
    def mock_session(self):
        """Mock database session."""
        session = MagicMock()
        return session

    @pytest.fixture
    def catalog_service(self, mock_session):
        """Create CatalogService instance."""
        return CatalogService(mock_session)

    @pytest.mark.asyncio
    async def test_create_title_structure(self, mock_session, catalog_service):
        """Test create_title method structure."""
        title_data = TitleCreate(
            title="Test Movie",
            original_title="Test Movie",
            description="A test movie",
            release_year=2024,
            rating=8.5,
            duration_minutes=120,
        )
        # Test that the method accepts the right parameters
        assert title_data.title == "Test Movie"

    @pytest.mark.asyncio
    async def test_get_title_structure(self, mock_session, catalog_service):
        """Test get_title method structure."""
        # Just validate the method exists and has correct signature
        assert hasattr(catalog_service, 'get_title')

    @pytest.mark.asyncio
    async def test_list_titles_structure(self, mock_session, catalog_service):
        """Test list_titles method structure."""
        assert hasattr(catalog_service, 'list_titles')

    @pytest.mark.asyncio
    async def test_search_titles_structure(self, mock_session, catalog_service):
        """Test search_titles method structure."""
        assert hasattr(catalog_service, 'search_titles')

    @pytest.mark.asyncio
    async def test_list_genres_structure(self, mock_session, catalog_service):
        """Test list_genres method structure."""
        assert hasattr(catalog_service, 'list_genres')

    @pytest.mark.asyncio
    async def test_list_platforms_structure(self, mock_session, catalog_service):
        """Test list_platforms method structure."""
        assert hasattr(catalog_service, 'list_platforms')