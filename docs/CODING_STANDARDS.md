# Coding Standards

## Python PEP 8 Compliance

### Line Length
- Maximum 88 characters for new code (PEP 8 recommendation)
- Existing code may be up to 100 characters
- Use line breaks to split long expressions

### Indentation
- 4 spaces per indentation level
- Never use tabs for indentation
- Consistent indentation within blocks

### Naming Conventions
- **Functions**: `lowercase_with_underscores()` (snake_case)
- **Variables**: `lowercase_with_underscores` (snake_case)
- **Classes**: `PascalCase` (UpperCamelCase)
- **Modules**: `lowercase_with_underscores.py`
- **Constants**: `UPPER_CASE` (all caps with underscores)
- **Enumerations**: `LowerCamelCase` or `UPPER_CASE`

### Imports
- Group imports in this order:
  1. Standard library imports (`os`, `sys`, `json`, etc.)
  2. Third-party imports (`fastapi`, `sqlalchemy`, `pytest`, etc.)
  3. Local application/library imports (`app.core`, `app.models`, etc.)
- Use blank lines to separate groups
- Use absolute imports within the project

```python
# Good
import abc
import json
from typing import Optional, List

import fastapi
import sqlalchemy
from fastapi import APIRouter, Depends

from app.core.config import Settings
from app.database.session import get_session
from app.models.user import User
```

### Type Hints
- All function parameters must have type hints
- All function return types must have type hints
- Use `Optional[X]` for nullable values
- Use `List[X]` for lists
- Use `Dict[K, V]` for dictionaries
- Use `Union[A, B]` for union types

```python
# Good
def get_user(user_id: int) -> Optional[User]:
    """Get a user by ID."""
    ...

# Bad - missing type hints
def get_user(user_id):
    return None
```

### Docstrings
- All modules, classes, functions, and methods must have docstrings
- Use Google-style docstrings or NumPy-style consistently
- Document parameters, return values, and raised exceptions

```python
# Good - Google style
def create_access_token(
    subject: str | int,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Create a JWT access token.
    
    Args:
        subject: The subject of the token (usually user email or ID)
        expires_delta: Optional timedelta for expiration
    
    Returns:
        Encoded JWT token string
    
    Raises:
        JWTError: If token encoding fails
    """
    ...
```

### Comments
- Use comments to explain "why" not "what"
- Keep comments concise and relevant
- Avoid obvious comments that the code already expresses

```python
# Good - explains business logic
# Skip users that are marked as inactive
# to avoid sending emails to closed accounts
```

### Error Handling
- Use HTTPException from FastAPI for API errors
- Include meaningful detail messages
- Use appropriate status codes
- Do not expose stack traces to clients

```python
# Good
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not found with email: {email}"
)
```

### Logging
- Use Python logging module
- Configure appropriate log levels
- Include relevant context in log messages
- Do not log sensitive data (passwords, tokens)

```python
import logging

logger = logging.getLogger(__name__)

logger.info("User registered successfully", extra={"user_id": user_id})
```

## FastAPI Specific Standards

### Route Organization
- Register all routes under `/api/v1/` prefix
- Use tags for grouping in Swagger UI
- Keep route functions focused on a single responsibility
- Dependencies injected via `Depends()`

### Response Models
- Always define response models with Pydantic
- Use `response_model` parameter in route decorators
- Return consistent response format

```python
# Good
@router.get("/", response_model=List[TitleRead])
async def list_titles(...) -> List[TitleRead]:
    ...
```

### Dependency Injection
- Use `Depends()` for dependency injection
- Keep dependencies focused and reusable
- Document dependencies in FILE_GUIDE.md

## Security Standards

### No Hardcoded Secrets
- Never commit passwords, API keys, or tokens
- Use environment variables via `.env` file
- `.env` file must be in `.gitignore`
- `.env.example` should have placeholder values only

```python
# Good - from environment
SECRET_KEY = Settings().SECRET_KEY

# Bad - hardcoded
SECRET_KEY = "super-secret-that-should-not-be-committed"
```

### Password Hashing
- Use Passlib or bcrypt for password hashing
- Never store plaintext passwords
- Use appropriate work factors

```python
# Good
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["auto"], deprecated="auto")
hashed = pwd_context.hash("plaintext_password")
verified = pwd_context.verify("entered_password", hashed)
```

### JWT Token Security
- Use strong secret keys (minimum 32 characters)
- Set appropriate expiration times
- Use HS256 or RS256 algorithms
- Include token type in response

```python
# Good
SECRET_KEY = "your-secret-key-change-in-production"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

## Testing Standards

### Test Organization
- Place tests in `tests/` directory
- Use conftest.py for fixtures
- Test both success and error cases
- Name test files descriptively: `test_*.py`

### Test Coverage
- Minimum 80% endpoint test coverage target
- Critical paths must have 100% coverage
- Include integration and unit tests

### Test Fixtures
- Use conftest.py for shared fixtures
- Create database session fixtures for tests
- Clean up test data after each test

```python
# Good conftest.py fixture
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_session, engine
from app.models import Base

@pytest.fixture(scope="function")
async def db_session():
    """Create a fresh database session for each test."""
    async with AsyncSession(engine) as session:
        async with session.begin():
            yield session
            # Rollback automatically after test
```

### HTTPX Testing
- Use httpx.AsyncClient for async tests
- Use httpx client for sync tests
- Include authentication headers when needed

```python
# Good
import httpx
import pytest

@pytest.mark.asyncio
async def test_register():
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/auth/register",
            json={"email": "test@example.com", "password": "password123"}
        )
        assert response.status_code == 201
```

## Git Standards

### Commit Messages
- Use imperative mood: "feat:", "fix:", "docs:"
- Include descriptive text when needed
- Reference related issues: "Closes #123"

### Branch Naming
- `feature/<description>` for new features
- `bugfix/<description>` for bug fixes
- `hotfix/<description>` for production fixes
- Never push directly to `main`

### Pull Requests
- Always create PR against `development` branch
- Fill in the PR template
- Include testing information
- Address review comments promptly

## Accessibility and Inclusion
- Code should be readable and maintainable
- Documentation should be clear and helpful
- Welcome contributions from all team members
- Follow the Code of Conduct