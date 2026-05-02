# EduCore ERP Backend - Makefile

.PHONY: install dev run test lint format migrate seed docker-up docker-down clean

# Install dependencies
install:
poetry install

# Run development server
dev:
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run production server
run:
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# Run tests
test:
poetry run pytest tests/ -v --cov=app --cov-report=html

# Lint code
lint:
poetry run black . --check
poetry run flake8 app

# Format code
format:
poetry run black .
poetry run isort .

# Run database migrations
migrate:
poetry run alembic upgrade head

# Create new migration
migration:
@read -p "Enter migration name: " name; \
poetry run alembic revision --autogenerate -m "$$name"

# Seed database with initial data
seed:
poetry run python scripts/seed.py

# Start Docker containers
docker-up:
docker-compose up -d

# Stop Docker containers
docker-down:
docker-compose down

# Restart Docker containers
docker-restart:
docker-compose down && docker-compose up -d

# View Docker logs
docker-logs:
docker-compose logs -f

# Clean Python cache
clean:
find . -type f -name "*.pyc" -delete
find . -type d -name "__pycache__" -delete
find . -type d -name ".pytest_cache" -delete
rm -rf htmlcov/
rm -rf .mypy_cache/

# Full setup for new developers
setup: install docker-up migrate seed
@echo "✅ Setup complete! Run 'make dev' to start the server"

# Show help
help:
@echo "EduCore ERP Backend - Available Commands:"
@echo "-------------------------------------------"
@echo "  make install      - Install dependencies"
@echo "  make dev          - Run development server"
@echo "  make run          - Run production server"
@echo "  make test         - Run tests"
@echo "  make lint         - Check code style"
@echo "  make format       - Format code"
@echo "  make migrate      - Run database migrations"
@echo "  make migration    - Create new migration"
@echo "  make seed         - Seed database with initial data"
@echo "  make docker-up    - Start Docker containers"
@echo "  make docker-down  - Stop Docker containers"
@echo "  make setup        - Full setup (install + docker + migrate + seed)"
@echo "  make clean        - Clean Python cache"
@echo "  make help         - Show this help message"
