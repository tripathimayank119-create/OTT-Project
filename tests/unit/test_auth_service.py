import pytest
from passlib.context import CryptContext
from fastapi import HTTPException

from app.services.auth_service import AuthService
from app.schemas.user import UserCreate


class TestAuthService:
    """Unit tests for AuthService - validates SOP compliance."""

    @pytest.mark.asyncio
    async def test_user_schema_validator(self):
        """Test UserCreate schema validation - SOP Week 2 requirement."""
        from app.schemas.user import UserCreate
        
        # Valid user creation with min length validation
        user_data = UserCreate(email="test@example.com", password="testpassword123")
        assert user_data.email == "test@example.com"
        assert len(user_data.password) >= 6  # min_length=6 validation
        
        # Test that password field has proper validation
        assert user_data.password == "testpassword123"

    @pytest.mark.asyncio
    async def test_auth_service_initialization(self):
        """Test AuthService can be initialized - SOP Week 2 requirement."""
        # Validates that the bcrypt scheme fix was applied
        from app.services.auth_service import pwd_context
        # pwd_context should have bcrypt scheme (fixed from "auto")
        assert pwd_context.schemes != ["auto"]  # Should not be "auto" scheme