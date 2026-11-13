# Git Collaboration Workflow

## Branching Strategy

```
main
  └── development
        ├── feature/database-models
        ├── feature/authentication
        ├── feature/catalog-crud
        ├── feature/search-redis
        ├── feature/background-sync
        └── feature/testing
```

## Branch Rules

### Protected Branches
- **main**: Protected - no direct pushes allowed
- **development**: Protected - feature branches merge into development via Pull Requests

### Feature Branches
- All feature branches must be created from `development`
- Naming convention: `feature/<feature-name>` or `bugfix/<bug-description>`
- Example: `feature/authentication`, `bugfix/search-filter`

### Workflow Steps

#### 1. Cloning the Repository
```bash
# Clone the repository
git clone https://github.com/your-username/ott-content-aggregator-api.git

# Change to project directory
cd ott-content-aggregator-api

# Add upstream remote if forked
git remote add upstream https://github.com/original-owner/ott-content-aggregator-api.git
```

#### 2. Creating a Feature Branch
```bash
# Ensure you're on development and it's up to date
git checkout development
git pull upstream development

# Create a new feature branch
git checkout -b feature/authentication

# Or from anywhere:
git switch development
git pull
git checkout -b feature/authentication
```

#### 3. Pulling Latest Development Changes
```bash
# Regularly update your feature branch with latest development
git checkout feature/authentication
git pull upstream development

# If there are conflicts, resolve them before continuing
```

#### 4. Committing Code
```bash
# Stage changed files
git add app/core/security.py app/repositories/title_repository.py

# Commit with meaningful message
git commit -m "feat: add JWT token creation and validation logic"

# Good commit message formats:
# "feat: add JWT authentication endpoints"
# "fix: resolve pagination edge case"
# "docs: update FILE_GUIDE.md with repository structure"
# "refactor: rename UserService to AuthService"
# "test: add user registration endpoint tests"
```

#### 5. Pushing Changes
```bash
# Push the feature branch to your fork
git push origin feature/authentication
```

#### 6. Opening Pull Requests
```bash
# Push feature branch, then create PR via GitHub UI or GitHub CLI
gh pr create \
  --title "feat: add JWT authentication" \
  --body "## Description
  
  Summary of changes:
  - Added JWT token creation in core/security.py
  - Added authentication dependencies in core/dependencies.py
  - Added auth endpoints in app/api/v1/endpoints/auth.py
  - Added auth service in app/services/auth_service.py
  
  ## Testing
  - Run: pytest tests/test_auth.py -v
  - Coverage: 85%
  
  ## Checklist
  - [ ] Code follows PEP 8 standards
  - [ ] Type hints included
  - [ ] Docstrings added
  - [ ] Tests written
  - [ ] No hardcoded secrets
  
  **Assignee**: @team-lead
  **Reviewer**: @team-lead"
```

#### 7. Resolving Merge Conflicts
```bash
# If conflicts occur during merge:
git checkout development
git pull upstream development

# Switch to feature branch
git checkout feature/authentication

# Merge development into feature branch
git merge upstream development

# Resolve conflicts in affected files
# Use: code editor to resolve <<<<< HEAD vs ======= vs >>>>> develop

# After resolving:
git add <resolved-files>
git commit -m "resolve: merge conflicts with development"

# Push and create Pull Request
git push origin feature/authentication
```

## Pull Request Process

1. **Create PR**: Push feature branch and open Pull Request against `development`
2. **Template**: Use the Pull Request template (see `.github/pull_request_template.md`)
3. **Review**: Team Lead reviews code, checks tests, verifies requirements
4. **Required Checks**: 
   - All CI checks must pass (linting, pytest)
   - No failing tests
   - Code coverage requirements met
5. **Approval**: Team Lead approves PR
6. **Merge**: Approved PR merged into `development`
7. **Delete Branch**: Feature branch deleted after merge

## Local Development Setup Commands

```bash
# Clone repository
git clone https://github.com/your-username/ott-content-aggregator-api.git
cd ott-content-aggregator-api

# Create development branch
git checkout -b development origin/development

# Install dependencies
pip install -r requirements-dev.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your local settings

# Start Docker (PostgreSQL + Redis)
docker-compose up -d

# Run migrations
alembic upgrade head

# Run the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Access Swagger UI at http://localhost:8000/docs
```

## Git Configuration Recommendations

```bash
# Set user identity
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Enable colored output
git config --global color.ui auto

# Set up pre-commit hooks (recommended)
pre-commit install

# Check for outdated pre-commit hooks
pre-commit autoupdate
```