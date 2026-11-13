# Development Guide

## Getting Started

### Prerequisites
- Docker and Docker Compose installed
- Python 3.12+ (if running without Docker)
- Git
- pip (Python package installer)

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/ott-content-aggregator-api.git
cd ott-content-aggregator-api
```

### 2. Create Development Branch
```bash
git checkout -b development origin/development
# Or if no upstream yet:
git checkout -b development
```

### 3. Install Dependencies
```bash
# Using pip
pip install -r requirements-dev.txt

# Or using pipenv/p poetry if configured
pipenv install --dev
```

### 4. Environment Configuration
```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your local settings
# Required variables:
#   DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost/ott_aggregator
#   REDIS_URL=redis://localhost:6379/0
#   SECRET_KEY=your-secret-key
#   ALGORITHM=HS256
#   ACCESS_TOKEN_EXPIRE_MINUTES=30
#   ENVIRONMENT=development
```

### 5. Start Docker Services
```bash
# Start PostgreSQL and Redis
docker-compose up -d

# Verify services are running
docker-compose ps
```

### 6. Run Database Migrations
```bash
alembic upgrade head
# Or to create a new migration:
alembic revision --autogenerate -m "description of changes"
```

### 7. Initialize the Application
```bash
# Start the FastAPI development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Access the application:
# - Swagger UI: http://localhost:8000/docs
# - ReDoc: http://localhost:8000/redoc
# - Health check: http://localhost:8000/
```

## Development Workflow

### Daily Operations
1. Start your day by pulling latest development changes:
   ```bash
   git checkout development
   git pull upstream development
   ```

2. Create a new feature branch:
   ```bash
   git checkout -b feature/<your-feature>
   ```

3. Implement the feature
4. Run tests frequently:
   ```bash
   pytest tests/ -v
   ```

5. Commit with meaningful messages
6. Push the branch
7. Open a Pull Request against `development`

### Code Editors and IDEs
- Use your preferred Python IDE (VS Code, PyCharm, etc.)
- Enable Python extensions for auto-completion
- Use black for code formatting: `black .`
- Use flake8 for linting: `flake8 .`
- Use isort for import sorting: `isort .`

### Testing
```bash
# Run all tests
pytest tests/ -v

# Run tests with coverage
pytest tests/ --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py -v

# Run specific test function
pytest tests/test_auth.py::test_register -v
```

### Linting and Formatting
```bash
# Check code style with black
black --check .

# Lint with flake8
flake8 .

# Sort imports with isort
isort .
```

## Docker Development

### Starting the Full Environment
```bash
docker-compose up -d
```

### Running Commands Inside Containers
```bash
# Run a shell inside the app container
docker-compose exec app sh

# Run migrations
docker-compose exec app alembic upgrade head

# Run tests inside container
docker-compose exec app pytest
```

### Stopping the Environment
```bash
docker-compose down
# To preserve data volumes:
docker-compose down -v
```

## Makefile Commands

| Command | Description |
|---|---|
| `make run` | Start the application with uvicorn |
| `make test` | Run pytest test suite |
| `make lint` | Run black and flake8 linting |
| `make docker-up` | Start Docker Compose services |
| `make docker-down` | Stop Docker Compose services |
| `make migrations` | Create new Alembic migration |
| `make coverage` | Generate test coverage report |
| `make clean` | Clean up temporary files |

## File Conventions

### Python Files
- Use `import ...` with proper grouping (standard, third-party, local)
- Include type hints for all function signatures
- Add docstrings to all classes, functions, and methods
- Follow PEP 8 line length (maximum 88 characters for new code)
- Use 4 spaces for indentation (no tabs)

### Naming Conventions
- **Modules**: lowercase_with_underscores.py
- **Classes**: PascalCase
- **Functions**: lowercase_with_underscores()
- **Variables**: lowercase_with_underscores
- **Constants**: UPPER_CASE
- **File names**: descriptive, English, lowercase

### Documentation
- All major files have corresponding README.md or documented in FILE_GUIDE.md
- API endpoints documented in API_DOCUMENTATION.md
- Database schema documented in DATABASE_SCHEMA.md
- Keep documentation updated with code changes

## Common Issues

### Docker Issues
- **Port already in use**: `docker-compose down` then `docker-compose up -d`
- **Connection refused**: Ensure PostgreSQL and Redis services are running
- **Migration errors**: Run `alembic upgrade head` fresh

### Python Issues
- **Module not found**: Run `pip install -r requirements.txt`
- **Import errors**: Ensure you're in the project directory
- **Type errors**: Check type hints and Python version compatibility

### Database Issues
- **Foreign key violations**: Check relationship definitions
- **Migration conflicts**: Use `alembic stamp` to fix head version
- **Connection errors**: Verify .env DATABASE_URL settings