
# OTT Content Aggregator API

A backend application for managing and aggregating movie and series catalogues across multiple OTT streaming platforms.

Built using FastAPI, PostgreSQL, SQLAlchemy, Alembic, Redis, and Python.

## Features

- User registration and login
- Secure password hashing using bcrypt
- JWT-based authentication
- Protected user profile endpoint
- Create, read, update, and delete OTT titles
- Genre management
- Streaming platform management
- Many-to-many relationships between titles, genres, and platforms
- Search and filtering by genre, platform, year, and featured status
- Pagination for catalogue results
- Redis caching for title-list responses
- Catalogue synchronization through a JSON API
- Interactive Swagger API documentation

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| FastAPI | REST API framework |
| PostgreSQL | Relational database |
| SQLAlchemy | Database ORM |
| Alembic | Database migrations |
| Pydantic | Data validation |
| Redis | Caching |
| JWT | Authentication |
| Passlib / bcrypt | Password hashing |
| Uvicorn | ASGI server |

## Project Structure

```text
OTT-Project/
│
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── auth.py
│   │       │   ├── users.py
│   │       │   ├── titles.py
│   │       │   ├── genres.py
│   │       │   ├── platforms.py
│   │       │   └── sync.py
│   │       └── routers.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   ├── dependencies.py
│   │   └── cache.py
│   │
│   ├── database/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   └── main.py
│
├── migrations/
│   └── versions/
│
├── requirements.txt
├── alembic.ini
├── .gitignore
└── README.md
```

## Prerequisites

Install the following before running the project:

- Python 3.10 or newer
- PostgreSQL
- Git
- Redis (optional, for caching)

## Installation

Clone the repository:

```bash
git clone https://github.com/tripathimayank119-create/OTT-Project.git
cd OTT-Project
git checkout feature/authentication
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Or use Git Bash:

```bash
source .venv/Scripts/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Configuration

Create a `.env` file in the project root.

Example:

```env
DATABASE_URL=postgresql+asyncpg://postgres:YOUR_PASSWORD@localhost:5432/ott_aggregator

REDIS_URL=redis://localhost:6379/0

SECRET_KEY=YOUR_LONG_RANDOM_SECRET_KEY

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30

ENV=development

DEBUG=True
```

Replace the database password and secret key with your own values.

Never commit `.env` or production credentials to GitHub.

## Database Setup

Create a PostgreSQL database named:

```sql
CREATE DATABASE ott_aggregator;
```

Apply database migrations:

```bash
alembic upgrade head
```

## Run the Application

Start the FastAPI development server:

```bash
python -m uvicorn app.main:app --reload
```

The application will run at:

http://127.0.0.1:8000

## API Documentation

FastAPI provides interactive API documentation through Swagger UI.

**Swagger UI:**

http://127.0.0.1:8000/docs

**ReDoc:**

http://127.0.0.1:8000/redoc

**Health Check:**

http://127.0.0.1:8000/

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | /auth/register | Register a new user |
| POST | /auth/login | Authenticate and receive JWT |

### Users

| Method | Endpoint | Description |
|---|---|---|
| GET | /users/me | Get authenticated user profile |

### Titles

| Method | Endpoint | Description |
|---|---|---|
| POST | /titles/ | Create a title |
| GET | /titles/ | List titles |
| GET | /titles/{title_id} | Get title details |
| PUT | /titles/{title_id} | Update a title |
| DELETE | /titles/{title_id} | Delete a title |

### Genres

| Method | Endpoint | Description |
|---|---|---|
| POST | /genres/ | Create a genre |
| GET | /genres/ | List genres |
| GET | /genres/{genre_id} | Get genre details |
| DELETE | /genres/{genre_id} | Delete a genre |

### Platforms

| Method | Endpoint | Description |
|---|---|---|
| POST | /platforms/ | Create a platform |
| GET | /platforms/ | List platforms |
| GET | /platforms/{platform_id} | Get platform details |
| DELETE | /platforms/{platform_id} | Delete a platform |

### Catalogue Synchronization

| Method | Endpoint | Description |
|---|---|---|
| POST | /sync/catalogue | Synchronize catalogue data |

## Catalogue Filtering

The title listing endpoint supports:

- `skip` – Pagination offset
- `limit` – Maximum number of records
- `genre_id` – Filter by genre
- `platform_id` – Filter by streaming platform
- `year` – Filter by release year
- `search` – Search by title
- `featured` – Filter featured titles

Example:

```text
GET /titles/?year=2014&featured=true
```

## Authentication Workflow

1. Register an account using `/auth/register`.
2. Log in using `/auth/login`.
3. Receive an access token.
4. Use the token through Swagger's Authorize option.
5. Access protected endpoints such as `/users/me`.

## Catalogue Synchronization

The synchronization endpoint accepts catalogue records as JSON.

It can:

- Add new titles.
- Update existing titles.
- Resolve genre names.
- Resolve streaming platform names.
- Associate titles with multiple genres and platforms.

This implementation uses request-driven synchronization. It does not currently fetch data directly from third-party OTT provider APIs or run on an automatic schedule.

## Caching

Redis is used as an optional caching layer for title-list responses.

- Cached responses have a configurable expiration.
- Catalogue changes invalidate title-list cache entries.
- The API continues operating if Redis is unavailable.

## Database Relationships

The application supports many-to-many relationships:

- One title can belong to multiple genres.
- One genre can be associated with multiple titles.
- One title can be available on multiple OTT platforms.
- One platform can contain multiple titles.

## Future Enhancements

- Integration with external OTT provider APIs
- Automated scheduled catalogue synchronization
- Advanced recommendation engine
- More detailed content metadata
- Production deployment and monitoring
- Expanded automated test coverage

## License

This project is developed for educational and demonstration purposes.
