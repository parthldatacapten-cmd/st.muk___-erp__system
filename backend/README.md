# EduCore Backend

FastAPI backend for EduCore ERP - Indian Education Management System.

## Setup

### Prerequisites
- Python 3.11+
- Poetry (package manager)
- Docker & Docker Compose

### Installation

```bash
# Install dependencies
poetry install

# Copy environment file
cp .env.example .env

# Start infrastructure (PostgreSQL, Redis, MinIO)
docker-compose up -d postgres redis minio

# Run database migrations
alembic upgrade head

# Start development server
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once running, access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health

## Project Structure

```
backend/
├── app/
│   ├── api/           # API routes
│   │   └── v1/
│   │       ├── endpoints/
│   │       └── router.py
│   ├── core/          # Configuration, security
│   │   ├── config.py
│   │   └── security.py
│   ├── db/            # Database session
│   │   └── session.py
│   ├── models/        # SQLAlchemy models
│   │   └── user.py
│   ├── schemas/       # Pydantic schemas
│   │   └── user.py
│   ├── services/      # Business logic
│   └── main.py        # FastAPI app
├── tests/             # Test files
├── pyproject.toml     # Dependencies
└── README.md
```

## Development

### Running Tests
```bash
poetry run pytest
```

### Code Formatting
```bash
poetry run black app/
poetry run isort app/
```

### Linting
```bash
poetry run flake8 app/
poetry run mypy app/
```

## Features Implemented (Sprint 0)

- ✅ Multi-tenancy support (Institutions)
- ✅ User authentication (JWT)
- ✅ Role-based access control
- ✅ User approval workflows
- ✅ Device binding (anti-fraud foundation)
- ✅ PostgreSQL + Redis setup
- ✅ Docker Compose configuration

## Next Steps (Sprint 1)

- Student registration & approval
- Batch/Class management
- Fee structure setup
- NFC attendance foundation
