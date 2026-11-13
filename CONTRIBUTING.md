# Contributing to OTT Content Aggregator API

## Development Guidelines

### Code Standards
- Follow PEP 8 Python coding standards
- Use type hints for all function parameters and return types
- Include docstrings for all classes, functions, and methods
- Avoid duplicate code - use modular architecture
- Keep files focused with single responsibilities

### Branch Management
- All work must be done on feature branches
- Branch naming: `feature/<feature-name>` or `bugfix/<description>`
- Create branches from `development`
- No direct pushes to `main`
- Pull Requests required for all changes

### Pull Request Process
1. Create a feature branch from `development`
2. Implement the feature with tests
3. Push the branch to your GitHub fork
4. Open a Pull Request against `development`
5. Fill in the PR template
6. Wait for Team Lead review and approval
5. Address any review comments
6. PR merged into `development` upon approval
7. Delete the feature branch

### Commit Message Convention
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `refactor:` Code restructuring
- `test:` Adding or fixing tests
- `chore:` Maintenance tasks
- `style:` Code style formatting

Example: `feat: add JWT authentication endpoints`

### Testing Requirements
- Write tests for all new functionality
- Minimum 80% test coverage target
- Use pytest for test framework
- Use httpx for API testing
- Test both success and error cases
- Run `pytest` before opening Pull Requests

### Code Review Checklist
- [ ] Code follows PEP 8 standards
- [ ] Type hints present
- [ ] Docstrings included
- [ ] Tests written and passing
- [ ] No hardcoded secrets or credentials
- [ ] No duplicate code
- [ ] Proper error handling
- [ ] API documentation updated if needed

### Issue Tracking
- Use GitHub Issues for bugs and feature requests
- Label issues appropriately (bug, feature, documentation, question)
- Link PRs to related issues
- Keep issue descriptions clear and reproducible

### Environment Setup
1. Clone the repository
2. Copy `.env.example` to `.env`
3. Edit `.env` with local configuration
4. Start Docker: `docker-compose up -d`
5. Run migrations: `alembic upgrade head`
6. Install dependencies: `pip install -r requirements-dev.txt`
7. Run the app: `uvicorn app.main:app --reload`

### Docker Commands
```bash
# Start all services (PostgreSQL + Redis + app)
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild services
docker-compose up -d --build
```

### Makefile Commands
```bash
make run          # Start the application
make test         # Run pytest
make lint         # Run linting (black, flake8)
make docker-up    # Start Docker services
make docker-down  # Stop Docker services
make migrations   # Create new Alembic migration
make coverage     # Generate test coverage report
```

### Code of Conduct
- Be respectful and inclusive
- Welcome contributors of all backgrounds
- Focus on constructive feedback
- Follow the project's Code of Conduct in `CODE_OF_CONDUCT.md`