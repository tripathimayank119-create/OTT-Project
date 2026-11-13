# File Guide

This document explains the purpose and responsibilities of every major Python file and folder in the repository.

## App Structure

### `app/__init__.py`
- **Purpose**: Root package file for the `app` Python module.
- **Implementation**: Empty file to make `app` a Python package.
- **Dependencies**: None.
- **Responsible**: Team Lead / Backend Architect.
- **Week**: Week 1.

### `app/core/__init__.py`
- **Purpose**: Root package file for the `core` module.
- **Implementation**: Empty file.
- **Dependencies**: None.

### `app/core/config.py`
- **Purpose**: Application configuration settings using Pydantic.
- **Implementation**: Contains `Settings`, `DevelopmentConfig`, and `ProductionConfig` classes with environment variable placeholders for DATABASE_URL, REDIS_URL, SECRET_KEY, ALGORITHM, and ACCESS_TOKEN_EXPIRE_MINUTES.
- **Dependencies**: `.env.example`.
- **Responsible**: Database Engineer (Member 2).
- **Week**: Week 1.

### `app/core/security.py`
- **Purpose**: JWT token creation and validation.
- **Implementation**: `create_access_token()` and `decode_access_token()` functions for encoding/decoding JWT tokens.
- **Dependencies**: `jose` library for JWT, `core/config.py` for settings.
- **Responsible**: Authentication & Security Developer (Member 3).
- **Week**: Week 2.

### `app/core/dependencies.py`
- **Purpose**: FastAPI dependency injection for database sessions and authentication.
- **Implementation**: `get_db_session()`, `get_current_user()`, and `get_optional_current_user()` dependency functions.
- **Dependencies**: `core/security.py`, `database/session.py`, models.
- **Responsible**: Authentication & Security Developer (Member 3).
- **Week**: Week 2.

### `app/database/__init__.py`
- **Purpose**: Root package file for the `database` module.
- **Implementation**: Empty file.
- **Dependencies**: None.

### `app/database/session.py`
- **Purpose**: Async SQLAlchemy engine and session management.
- **Implementation**: `engine` (AsyncEngine), `SessionLocal` sessionmaker, and `get_session()` generator function for dependency injection.
- **Dependencies**: `core/config.py` for DATABASE_URL.
- **Responsible**: Database Engineer (Member 2).
- **Week**: Week 1.

### `app/database/base.py`
- **Purpose**: Base class for all SQLAlchemy models.
- **Implementation**: Uses `@as_declarative()` decorator from SQLAlchemy 2.0.
- **Dependencies**: SQLAlchemy 2.0.
- **Responsible**: Database Engineer (Member 2).
- **Week**: Week 1.

### `app/models/__init__.py`
- **Purpose**: Root package file for the `models` module.
- **Implementation**: Empty file.
- **Dependencies**: None.

### `app/models/user.py`
- **Purpose**: SQLAlchemy User model.
- **Implementation**: `User` class with fields: id, email, hashed_password, is_active, is_superuser, created_at, updated_at. Includes unique email constraint.
- **Dependencies**: `database/base.py`.
- **Responsible**: Database Engineer (Member 2).
- **Week**: Week 1.

### `app/models/title.py`
- **Purpose**: SQLAlchemy models for Title, Genre, Platform, and TitleGenre junction table.
- **Implementation**: 
  - `Genre`: id, name, description, created_at
  - `Platform`: id, name, slug, description, created_at
  - `Title`: id, title, original_title, description, release_year, rating, duration_minutes, is_featured, genre_id, platform_id, created_at, updated_at
  - `TitleGenre`: junction table for many-to-many relationship between titles and genres
- **Dependencies**: `database/base.py`.
- **Responsible**: Database Engineer (Member 2).
- **Week**: Week 1.

### `app/models/platform.py`
- **Purpose**: Placeholder for additional platform-related models.
- **Implementation**: Currently empty, extensible for future use.
- **Dependencies**: None.
- **Responsible**: Database Engineer (Member 2).
- **Week**: Week 1.

### `app/schemas/__init__.py`
- **Purpose**: Root package file for the `schemas` module.
- **Implementation**: Empty file.
- **Dependencies**: None.

### `app/schemas/user.py`
- **Purpose**: Pydantic schemas for User entities.
- **Implementation**:
  - `UserBase`: Base fields (email, password).
  - `UserCreate`: User creation schema.
  - `UserRead`: User read schema with id, email, is_active, is_superuser, created_at.
  - `UserLogin`: Login schema with email and password.
- **Dependencies**: None.
- **Responsible**: Authentication & Security Developer (Member 3).
- **Week**: Week 2.

### `app/schemas/title.py`
- **Purpose**: Pydantic schemas for Title, Genre, and Platform entities.
- **Implementation**:
  - `GenreBase`, `GenreCreate`, `GenreRead`: Genre schema with id, name, description, created_at.
  - `PlatformBase`, `PlatformCreate`, `PlatformRead`: Platform schema with id, name, slug, description, created_at.
  - `TitleBase`: Base title fields (title, original_title, description, release_year, rating, duration_minutes, is_featured, genre_ids, platform_ids).
  - `TitleCreate`: Title creation schema.
  - `TitleRead`: Title read schema with relationships to Genre and Platform.
  - `TitleUpdate`: Title update schema with optional fields and genre_ids/platform_ids.
- **Dependencies**: None.
- **Responsible**: Catalog API Developer (Member 4).
- **Week**: Week 2.

### `app/api/__init__.py`
- **Purpose**: Root package file for the `api` module.
- **Implementation**: Empty file.
- **Dependencies**: None.

### `app/api/v1/__init__.py`
- **Purpose**: Root package file for the `api.v1` module.
- **Implementation**: Empty file.
- **Dependencies**: None.

### `app/api/v1/routers.py`
- **Purpose**: API router registration container.
- **Implementation**: Defines individual routers (auth, users, titles, genres, platforms, search, sync) and `include_routers()` function to register them all into the FastAPI app.
- **Dependencies**: All endpoint modules in `app/api/v1/endpoints/`.
- **Responsible**: Backend Architect (Team Lead).
- **Week**: Week 2.

### `app/api/v1/endpoints/__init__.py`
- **Purpose**: Root package file for endpoint modules.
- **Implementation**: Empty file.
- **Dependencies**: None.

### `app/api/v1/endpoints/auth.py`
- **Purpose**: Authentication endpoints (register, login).
- **Implementation**: 
  - `POST /auth/register`: Register new user with email/password.
  - `POST /auth/login`: Login with email/password and receive JWT token.
- **Dependencies**: `core/security.py`, `repositories/user_repository.py`, `schemas/user.py`, `services/auth_service.py`.
- **Responsible**: Authentication & Security Developer (Member 3).
- **Week**: Week 2.

### `app/api/v1/endpoints/users.py`
- **Purpose**: User profile endpoint.
- **Implementation**:
  - `GET /users/me`: Get current authenticated user profile using JWT dependency.
- **Dependencies**: `core/dependencies.py`, `schemas/user.py`.
- **Responsible**: Authentication & Security Developer (Member 3).
- **Week**: Week 2.

### `app/api/v1/endpoints/titles.py`
- **Purpose**: Title (movie/TV show) CRUD endpoints.
- **Implementation**:
  - `POST /titles/`: Create a new title.
  - `GET /titles/`: List all titles with pagination.
  - `GET /titles/{title_id}`: Get a specific title by ID.
- **Dependencies**: `database/session.py`, `models/title.py`, `schemas/title.py`, `repositories/title_repository.py`, `services/catalog_service.py`.
- **Responsible**: Catalog API Developer (Member 4).
- **Week**: Week 2.

### `app/api/v1/endpoints/genres.py`
- **Purpose**: Genre endpoints.
- **Implementation**:
  - `GET /genres/`: List all genres.
- **Dependencies**: `database/session.py`, `models/title.py`, `repositories/title_repository.py`.
- **Responsible**: Catalog API Developer (Member 4).
- **Week**: Week 2.

### `app/api/v1/endpoints/platforms.py`
- **Purpose**: OTT Platform endpoints.
- **Implementation**:
  - `GET /platforms/`: List all OTT platforms.
- **Dependencies**: `database/session.py`, `models/title.py`, `repositories/title_repository.py`.
- **Responsible**: Catalog API Developer (Member 4).
- **Week**: Week 2.

### `app/api/v1/endpoints/search.py`
- **Purpose**: Search endpoints for titles with filtering.
- **Implementation**:
  - `GET /search/`: Search titles with query, genre_id, platform_id, and release_year filters.
- **Dependencies**: `database/session.py`, `models/title.py`, `repositories/title_repository.py`.
- **Responsible**: Search & Performance Developer (Member 5).
- **Week**: Week 3.

### `app/services/__init__.py`
- **Purpose**: Root package file for the `services` module.
- **Implementation**: Empty file.
- **Dependencies**: None.

### `app/services/auth_service.py`
- **Purpose**: Authentication business logic.
- **Implementation**: `AuthService` class with `register()` and `login()` methods handling user registration, password hashing, and JWT token generation.
- **Dependencies**: `core/security.py`, `repositories/user_repository.py`, `schemas/user.py`, `passlib` for password hashing.
- **Responsible**: Authentication & Security Developer (Member 3).
- **Week**: Week 2.

### `app/services/catalog_service.py`
- **Purpose**: Catalog business logic for managing titles.
- **Implementation**: `CatalogService` class with `create_title()`, `get_title()`, `list_titles()`, `search_titles()`, `list_genres()`, `list_platforms()` methods.
- **Dependencies**: `database/session.py`, `models/title.py`, `repositories/title_repository.py`.
- **Responsible**: Catalog API Developer (Member 4).
- **Week**: Week 2.

### `app/services/search_service.py`
- **Purpose**: Advanced search business logic.
- **Implementation**: `SearchService` class with `advanced_search()` method supporting multiple filter parameters.
- **Dependencies**: `database/session.py`, `models/title.py`, `repositories/title_repository.py`.
- **Responsible**: Search & Performance Developer (Member 5).
- **Week**: Week 3.

### `app/services/cache_service.py`
- **Purpose**: Redis cache service for search results and popular content.
- **Implementation**: `CacheService` class with `get()`, `set()`, `invalidate()`, and `get_popular_searches()` methods (Redis integration placeholders).
- **Dependencies**: Redis, `repositories/title_repository.py`.
- **Responsible**: Search & Performance Developer (Member 5).
- **Week**: Week 3.

### `app/services/sync_service.py`
- **Purpose**: Background synchronization service for OTT platform data.
- **Implementation**: `SyncService` class with `sync_titles()` and `force_sync()` methods for simulating external OTT platform synchronization.
- **Dependencies**: `database/session.py`, `models/title.py`, `repositories/title_repository.py`.
- **Responsible**: Background Tasks & QA Developer (Member 6).
- **Week**: Week 4.

### `app/repositories/__init__.py`
- **Purpose**: Root package file for the `repositories` module.
- **Implementation**: Empty file.
- **Dependencies**: None.

### `app/repositories/user_repository.py`
- **Purpose**: User data access layer.
- **Implementation**: `UserRepository` class with `get_by_email()` and `create()` methods for database operations on User model.
- **Dependencies**: `database/session.py`, `models/user.py`.
- **Responsible**: Database Engineer (Member 2).
- **Week**: Week 1.

### `app/repositories/title_repository.py`
- **Purpose**: Title data access layer with search functionality.
- **Implementation**: `TitleRepository` class with `get_by_id()`, `get_all()`, `search()`, `get_genres()`, `get_platforms()` methods for Title, Genre, and Platform database operations.
- **Dependencies**: `database/session.py`, `models/title.py`.
- **Responsible**: Database Engineer (Member 2).
- **Week**: Week 1.

### `app/tasks/__init__.py`
- **Purpose**: Root package file for the `tasks` module.
- **Implementation**: Empty file.
- **Dependencies**: None.

### `app/tasks/sync_tasks.py`
- **Purpose**: Background sync tasks for OTT platform data simulation.
- **Implementation**: `sync_ott_data()` async function using FastAPI BackgroundTasks to simulate external OTT platform synchronization.
- **Dependencies**: `services/sync_service.py`.
- **Responsible**: Background Tasks & QA Developer (Member 6).
- **Week**: Week 4.

### `app/utils/__init__.py`
- **Purpose**: Root package file for the `utils` module.
- **Implementation**: Empty file.
- **Dependencies**: None.

### `app/utils/pagination.py`
- **Purpose**: Pagination utility functions and models.
- **Implementation**:
  - `PaginationParams`: Pydantic model for skip/limit parameters.
  - `PaginationResponse`: Pydantic response model with items, total, page, per_page, total_pages.
  - `paginate()`: Function to calculate pagination metadata and slice items.
- **Dependencies**: None.
- **Responsible**: Backend Architect (Team Lead).
- **Week**: Week 3.

## Core Folders

### `migrations/`
- **Purpose**: Alembic database migration directory.
- **Implementation**: Contains migration scripts for database schema changes. `alembic.ini` at root configures migration behavior.
- **Dependencies**: SQLAlchemy 2.0, Alembic.
- **Responsible**: Database Engineer (Member 2).
- **Week**: Week 1.

### `tests/`
- **Purpose**: Pytest test directory.
- **Implementation**: Contains test files for all API endpoints and functionality.
- **Dependencies**: `pytest`, `httpx`, `httpx[async]`.
- **Responsible**: Background Tasks & QA Developer (Member 6).
- **Week**: Week 4.

### `docs/`
- **Purpose**: All project documentation.
- **Implementation**: See individual documentation files in this directory.
- **Dependencies**: None.
- **Responsible**: Team Lead / Backend Architect.
- **Week**: Week 1.

### `scripts/`
- **Purpose**: Helper scripts for development operations.
- **Implementation**: Makefile commands, database initialization scripts, etc.
- **Dependencies**: None.
- **Responsible**: Team Lead / Backend Architect.
- **Week**: Week 1.

### `.github/`
- **Purpose**: GitHub Actions and workflow configuration.
- **Implementation**: CI/CD workflows, issue templates, pull request template.
- **Dependencies**: None.
- **Responsible**: Team Lead / Backend Architect.
- **Week**: Week 1.

## Configuration Files

### `.env.example`
- **Purpose**: Environment variable templates for development.
- **Implementation**: Placeholders for DATABASE_URL, REDIS_URL, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, ENVIRONMENT.
- **Dependencies**: None.
- **Responsible**: Team Lead / Backend Architect.
- **Week**: Week 1.

### `Dockerfile`
- **Purpose**: Docker container configuration for the application.
- **Implementation**: Multi-stage build or simple Python runtime with uvicorn.
- **Dependencies**: None.
- **Responsible**: DevOps / Team Lead.
- **Week**: Week 1.

### `docker-compose.yml`
- **Purpose**: Docker Compose configuration for PostgreSQL, Redis, and the application.
- **Implementation**: Services for postgres, redis, and the FastAPI app with volume mappings and network configuration.
- **Dependencies**: Docker, Docker Compose.
- **Responsible**: DevOps / Team Lead.
- **Week**: Week 1.

### `alembic.ini`
- **Purpose**: Alembic configuration file for database migrations.
- **Implementation**: Configures migration directory, URL, and template settings.
- **Dependencies**: Alembic, SQLAlchemy.
- **Responsible**: Database Engineer (Member 2).
- **Week**: Week 1.

### `pyproject.toml`
- **Purpose**: Project configuration for Poetry or tool configuration.
- **Implementation**: Project metadata, dependencies, tool configuration (black, flake8, mypy).
- **Dependencies**: None.
- **Responsible**: Team Lead / Backend Architect.
- **Week**: Week 1.

### `requirements.txt`
- **Purpose**: Production Python dependencies.
- **Implementation**: FastAPI, SQLAlchemy, Pydantic, etc.
- **Dependencies**: None.
- **Responsible**: Team Lead / Backend Architect.
- **Week**: Week 1.

### `requirements-dev.txt`
- **Purpose**: Development dependencies for linting, testing, formatting.
- **Implementation**: Pytest, black, flake8, mypy, pre-commit, etc.
- **Dependencies**: None.
- **Responsible**: Team Lead / Backend Architect.
- **Week**: Week 1.

### `.gitignore`
- **Purpose**: Git ignore patterns.
- **Implementation**: Python, Virtual Environment, Docker, IDE patterns.
- **Dependencies**: None.
- **Responsible**: Team Lead / Backend Architect.
- **Week**: Week 1.

### `Makefile`
- **Purpose**: Development commands shortcuts.
- **Implementation**: `make run`, `make test`, `make lint`, `make docker-up`, `make docker-down` commands.
- **Dependencies**: None.
- **Responsible**: Team Lead / Backend Architect.
- **Week**: Week 1.