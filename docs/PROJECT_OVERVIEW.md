# Project Overview: OTT Content Aggregator API

## Description
High-performance asynchronous REST API that aggregates movies and TV shows from multiple OTT platforms into a unified content catalog. Users can register, authenticate, search movies and shows, filter by genre, release year, and OTT platform, and discover where content is available.

## Technology Stack
- **Python 3.12+**: Core programming language
- **FastAPI**: Modern web framework for building APIs with Python 3.10+
- **Pydantic v2**: Data validation and settings management using Python type hints
- **SQLAlchemy 2.0 (Async)**: SQL toolkit and ORM with async support
- **PostgreSQL**: Relational database for persistent storage
- **Alembic**: Database migration tool
- **Redis**: In-memory data structure store for caching
- **JWT Authentication**: JSON Web Tokens for secure authentication
- **Passlib**: Password hashing library
- **HTTPX**: Asynchronous HTTP client for API requests and testing
- **Pytest**: Testing framework
- **Docker and Docker Compose**: Containerization and orchestration
- **Uvicorn**: ASGI server for FastAPI

## Architecture
The application follows clean architecture with separation of concerns:
- **Presentation Layer**: FastAPI endpoints (API routes)
- **Business Logic Layer**: Services (catalog_service, auth_service, search_service, etc.)
- **Data Access Layer**: Repositories (user_repository, title_repository)
- **Database Layer**: SQLAlchemy 2.0 async models and sessions
- **Cache Layer**: Redis for caching popular search results
- **Background Layer**: Tasks for OTT platform synchronization

## Features
- User registration and JWT authentication
- Movie and TV show CRUD operations
- Genre and OTT platform filtering
- Advanced search with multiple filters
- Redis caching for search results
- Background task simulation of OTT platform sync
- Swagger UI and ReDoc documentation
- Dockerized development environment

## API Base Path
All endpoints are prefixed with `/api/v1/`

## Development
Six-member team with defined roles:
1. Team Lead / Backend Architect
2. Database Engineer
3. Authentication & Security Developer
4. Catalog API Developer
5. Search & Performance Developer
6. Background Tasks & QA Developer