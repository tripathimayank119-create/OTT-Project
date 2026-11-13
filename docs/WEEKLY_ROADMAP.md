# Weekly Roadmap

## Week 1 – Setup and Database Modeling

### Focus
Project initialization, folder structure, and database foundation.

### Key Tasks
- FastAPI scaffolding and project setup
- Folder structure creation and configuration
- SQLAlchemy 2.0 async models definition
- Pydantic schemas creation
- PostgreSQL connection via Docker Compose
- Alembic configuration for migrations
- Swagger UI accessibility

### Team Member Assignments
| Member | Focus Area |
|---|---|
| Team Lead | Repository creation, overall scaffolding, Makefile |
| DB Engineer (M2) | SQLAlchemy models, Alembic config, PostgreSQL |
| Auth Developer (M3) | Password hashing setup, auth schemas |
| Catalog Dev (M4) | Title schemas, repository placeholders |
| Search Dev (M5) | Search service placeholders |
| QA Developer (M6) | Test configuration, fixtures |

### Success Criteria
- ✅ Repository accessible in GitHub
- ✅ `uvicorn app.main:app --reload` starts without errors
- ✅ Swagger UI at `/docs` working
- ✅ `alembic upgrade head` runs successfully
- ✅ All models and schemas defined per specification

---

## Week 2 – CRUD and Authentication

### Focus
User authentication and title CRUD operations.

### Key Tasks
- User registration and login with JWT
- Protected routes implementation
- Movie and show CRUD endpoints
- Genre and platform API endpoints

### Team Member Assignments
| Member | Focus Area |
|---|---|
| Team Lead | PR reviews, integration, app.main configuration |
| DB Engineer (M2) | User repository, search refinements |
| Auth Developer (M3) | JWT creation/validation, login/register |
| Catalog Dev (M4) | Title CRUD, genre/platform endpoints |
| Search Dev (M5) | Search endpoint placeholders |
| QA Developer (M6) | Auth tests, HTTPX testing |

### Success Criteria
- ✅ `POST /api/v1/auth/register` working
- ✅ `POST /api/v1/auth/login` working with JWT
- ✅ `GET /api/v1/users/me` protected endpoint
- ✅ `POST /api/v1/titles/` CRUD functional
- ✅ `GET /api/v1/genres/` and `GET /api/v1/platforms/` working
- ✅ Test coverage for auth endpoints

---

## Week 3 – Search and Redis

### Focus
Advanced search functionality and caching.

### Key Tasks
- Advanced filtering and search queries
- Redis integration for cache
- Cache invalidation strategies
- Performance optimization

### Team Member Assignments
| Member | Focus Area |
|---|---|
| Team Lead | Review search PRs, ensure integration |
| DB Engineer (M2) | Query optimization, indexing |
| Auth Developer (M3) | Search endpoint auth as needed |
| Catalog Dev (M4) | Complete genre/platform features |
| Search Dev (M5) | Search service, Redis caching, advanced filters |
| QA Developer (M6) | Search tests, performance testing |

### Success Criteria
- ✅ `GET /api/v1/search/` with query parameters working
- ✅ Redis cache service integrated
- ✅ Advanced search with multiple filters
- ✅ Performance improvements documented

---

## Week 4 – Background Tasks and Testing

### Focus
OTT synchronization, comprehensive testing, and polish.

### Key Tasks
- OTT synchronization simulation background task
- Pytest test suite development
- HTTPX API testing
- 80%+ endpoint test coverage target
- Final integration and bug fixing

### Team Member Assignments
| Member | Focus Area |
|---|---|
| Team Lead | Final integration, deployment preparation |
| DB Engineer (M2) | Final optimizations, migration review |
| Auth Developer (M3) | Security review, no hardcoded secrets |
| Catalog Dev (M4) | Final catalog feature completion |
| Search Dev (M5) | Performance testing, cache validation |
| QA Developer (M6) | Comprehensive test suite, 80% coverage, performance reporting |

### Success Criteria
- ✅ OTT sync background task implemented
- ✅ Pytest suite covering all endpoints
- ✅ Test coverage >= 80%
- ✅ HTTPX tests passing
- ✅ No critical bugs remaining
- ✅ Final integration complete
- ✅ Documentation complete

### Final Delivery
- ✅ GitHub repository complete
- ✅ All documentation files created
- ✅ Docker environment functional
- ✅ GitHub Actions CI workflow
- ✅ Six-member role allocation
- ✅ Branching workflow documented
- ✅ Roadmap completed