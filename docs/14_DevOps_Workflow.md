# 14. Development Workflow & DevOps Guide

## 1. Version Control Strategy

### 1.1 Branching Model (GitFlow-Inspired)

```
main (Production)
 │
 ├── develop (Integration)
 │    │
 │    ├── feature/user-authentication
 │    ├── feature/qr-attendance
 │    ├── feature/fee-payment
 │    ├── bugfix/login-crash
 │    └── hotfix/security-patch
 │
 └── release/v1.0.0 (Staging)
```

### 1.2 Branch Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| **Feature** | `feature/{ticket-id}-{short-desc}` | `feature/EDU-101-qr-attendance` |
| **Bugfix** | `bugfix/{ticket-id}-{short-desc}` | `bugfix/EDU-205-login-crash` |
| **Hotfix** | `hotfix/{ticket-id}-{short-desc}` | `hotfix/EDU-301-security-patch` |
| **Release** | `release/v{major}.{minor}.{patch}` | `release/v1.0.0` |
| **Documentation** | `docs/{short-desc}` | `docs/api-examples` |

### 1.3 Commit Message Convention (Conventional Commits)

```
<type>(<scope>): <subject>

<body>

<footer>
```

#### Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style (formatting, semicolons)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

#### Examples:
```bash
feat(attendance): add QR code generation endpoint

- Implement dynamic QR generation with 30s expiry
- Add geo-fencing validation
- Add selfie challenge trigger logic

Closes EDU-101

---

fix(auth): resolve JWT token expiration issue

- Extend refresh token validity to 7 days
- Add automatic token rotation
- Fix race condition in token refresh

Fixes EDU-205

---

docs(api): add attendance API examples

- Add request/response samples for all endpoints
- Include error handling examples
- Add rate limiting documentation
```

### 1.4 Pull Request Workflow

#### PR Template (.github/PULL_REQUEST_TEMPLATE.md)
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] 🐛 Bug fix
- [ ] ✨ New feature
- [ ] 💥 Breaking change
- [ ] 📝 Documentation update
- [ ] ♻️ Refactoring
- [ ] ✅ Tests added

## Testing Done
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Screenshots (if UI changes)
Before: 
After:

## Checklist
- [ ] Code follows project guidelines
- [ ] Self-review completed
- [ ] Comments added where necessary
- [ ] Documentation updated
- [ ] No new warnings
- [ ] Tests added for new functionality
```

#### PR Review Process:
1. **Author**: Creates PR from `feature/*` → `develop`
2. **CI Pipeline**: Runs automated tests, linting, security scans
3. **Reviewer 1**: Tech lead review (required)
4. **Reviewer 2**: Peer review (required for critical features)
5. **QA**: Testing on staging environment
6. **Merge**: Squash merge to `develop` branch
7. **Deploy**: Automatic deployment to staging

### 1.5 Code Review Guidelines

#### Reviewer Checklist:
- [ ] Code follows design patterns documented in FRDs
- [ ] No hardcoded values (use environment variables)
- [ ] Error handling implemented
- [ ] Logging added for debugging
- [ ] Security considerations addressed
- [ ] Performance implications considered
- [ ] Backward compatibility maintained
- [ ] API documentation updated

#### Review Response Time SLA:
- **Critical/Hotfix**: Within 2 hours
- **Standard Feature**: Within 24 hours
- **Documentation**: Within 48 hours

---

## 2. Development Environment Setup

### 2.1 Prerequisites

```bash
# Required Software
- Python 3.11+
- Node.js 20 LTS
- Docker & Docker Compose
- PostgreSQL 16+
- Redis 7+
- Git

# Recommended IDE
- VS Code with extensions:
  - Python (ms-python.python)
  - Pylance (ms-python.vscode-pylance)
  - Black Formatter (ms-python.black-formatter)
  - ESLint (dbaeumer.vscode-eslint)
  - Prettier (esbenp.prettier-vscode)
  - Docker (ms-azuretools.vscode-docker)
  - GitLens (eamodio.gitlens)
```

### 2.2 Local Development Setup

```bash
# Clone repository
git clone https://github.com/parthldatacapten-cmd/st.muk___-erp__system.git
cd st.muk___-erp__system
git checkout qwen_coder_

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with local configurations

# Frontend setup
cd ../frontend
npm install
cp .env.example .env.local

# Database setup
docker-compose up -d postgres redis

# Run migrations
alembic upgrade head

# Start development servers
# Terminal 1 (Backend)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 (Frontend)
npm run dev

# Access applications
# Backend API: http://localhost:8000
# Frontend Web: http://localhost:3000
# Swagger Docs: http://localhost:8000/docs
```

### 2.3 Environment Variables Template

#### Backend (.env)
```env
# Application
APP_NAME=EduCore ERP
ENVIRONMENT=development
DEBUG=True
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/educore_dev

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Storage (S3-compatible)
STORAGE_ENDPOINT=minio:9000
STORAGE_ACCESS_KEY=minioadmin
STORAGE_SECRET_KEY=minioadmin
STORAGE_BUCKET=educore-dev

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=noreply@educore.in
SMTP_PASSWORD=app-password

# SMS Gateway
SMS_PROVIDER=textlocal
SMS_API_KEY=your-api-key
SMS_SENDER_ID=EDUCOR

# Payment Gateway
RAZORPAY_KEY_ID=rzp_test_xxxxx
RAZORPAY_KEY_SECRET=xxxxx
RAZORPAY_WEBHOOK_SECRET=xxxxx

# Monitoring
SENTRY_DSN=https://xxxxx@sentry.io/xxxxx
LOG_LEVEL=DEBUG
```

#### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws
NEXT_PUBLIC_ENVIRONMENT=development
NEXT_PUBLIC_SENTRY_DSN=https://xxxxx@sentry.io/xxxxx
```

---

## 3. Code Quality & Linting

### 3.1 Python Linting Configuration

#### pyproject.toml
```toml
[tool.black]
line-length = 100
target-version = ['py311']
include = '\.pyi?$'
exclude = '''
/(
    \.git
  | \.venv
  | __pycache__
)/
'''

[tool.isort]
profile = "black"
line_length = 100
multi_line_output = 3
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true
ensure_newline_before_comments = true

[tool.ruff]
line-length = 100
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # Pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
]
ignore = [
    "E501",  # line too long (handled by black)
    "B008",  # do not perform function calls in argument defaults
]

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true

[[tool.mypy.overrides]]
module = ["tests.*"]
disallow_untyped_defs = false
```

### 3.2 JavaScript/TypeScript Linting

#### .eslintrc.json
```json
{
  "extends": [
    "next/core-web-vitals",
    "plugin:@typescript-eslint/recommended",
    "prettier"
  ],
  "parser": "@typescript-eslint/parser",
  "plugins": ["@typescript-eslint"],
  "rules": {
    "@typescript-eslint/no-unused-vars": ["error", { "argsIgnorePattern": "^_" }],
    "@typescript-eslint/explicit-function-return-type": "warn",
    "react/react-in-jsx-scope": "off",
    "no-console": ["warn", { "allow": ["warn", "error"] }]
  }
}
```

#### .prettierrc
```json
{
  "semi": false,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 100,
  "arrowParens": "always"
}
```

### 3.3 Pre-commit Hooks

#### .pre-commit-config.yaml
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: ['--maxkb=1000']

  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.1.9
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]

  - repo: local
    hooks:
      - id: pytest-check
        name: Run pytest
        entry: pytest
        language: system
        pass_filenames: false
        always_run: true
        args: ["-x", "--cov=app", "--cov-report=term-missing"]
```

#### Install pre-commit hooks:
```bash
pip install pre-commit
pre-commit install
pre-commit install --hook-type commit-msg
```

---

## 4. Testing Strategy

### 4.1 Testing Pyramid

```
           ╱╲
          /  \         E2E Tests (10%)
         /----\        Playwright, Cypress
        /      \
       /        \      Integration Tests (20%)
      /----------\     API tests, DB integration
     /            \
    /--------------\   Unit Tests (70%)
   /                \  pytest, jest
  /__________________\
```

### 4.2 Unit Testing (Python)

#### tests/test_attendance.py
```python
import pytest
from datetime import datetime, timedelta
from app.services.attendance import AttendanceService
from app.models.session import AttendanceSession

@pytest.mark.asyncio
async def test_generate_dynamic_qr():
    """Test QR code generation with correct expiry"""
    service = AttendanceService()
    
    session = await service.create_session(
        batch_id="BATCH_001",
        subject_id="SUB_001",
        duration_seconds=30
    )
    
    assert session.qr_code is not None
    assert session.valid_until > datetime.utcnow()
    assert session.valid_until <= datetime.utcnow() + timedelta(seconds=30)

@pytest.mark.asyncio
async def test_mark_attendance_proxy_detection():
    """Test proxy detection when device ID mismatches"""
    service = AttendanceService()
    
    with pytest.raises(ProxyDetectionError) as exc_info:
        await service.mark_attendance(
            session_id="SES_001",
            student_id="STU_001",
            device_id="android_fake123",  # Mismatched device
            location={"lat": 18.52, "lng": 73.85}
        )
    
    assert exc_info.value.reason == "device_mismatch"
    assert exc_info.value.action_required == "upload_selfie"
```

### 4.3 Integration Testing

#### tests/integration/test_fee_payment.py
```python
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_fee_payment_creates_immutable_record():
    """Test that fee payments cannot be deleted, only reversed"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        
        # Create payment
        response = await client.post("/api/v1/fees/payments", json={
            "invoice_id": "INV_001",
            "amount_paid": 50000,
            "payment_mode": "upi"
        })
        
        assert response.status_code == 201
        payment_id = response.json()["payment_id"]
        
        # Try to delete (should fail)
        delete_response = await client.delete(f"/api/v1/fees/payments/{payment_id}")
        assert delete_response.status_code == 405  # Method not allowed
        
        # Reverse instead
        reverse_response = await client.post(
            f"/api/v1/fees/payments/{payment_id}/reverse",
            json={"reason": "Test reversal"}
        )
        
        assert reverse_response.status_code == 200
        
        # Verify original record still exists
        get_response = await client.get(f"/api/v1/fees/payments/{payment_id}")
        assert get_response.json()["status"] == "reversed"
        assert get_response.json()["reversal_id"] is not None
```

### 4.4 End-to-End Testing (Playwright)

#### tests/e2e/test_attendance_flow.spec.ts
```typescript
import { test, expect } from '@playwright/test';

test.describe('QR Attendance Flow', () => {
  test('teacher generates QR and student marks attendance', async ({ page, context }) => {
    // Teacher login
    await page.goto('/login');
    await page.fill('[name=email]', 'teacher@stxaviers.edu.in');
    await page.fill('[name=password]', 'TeacherPass123!');
    await page.click('button[type=submit]');
    
    // Navigate to attendance marking
    await page.click('text=Mark Attendance');
    await page.selectOption('select[name=batch]', 'BATCH_SCI_001');
    await page.click('button:has-text("Start Session")');
    
    // Wait for QR code to appear
    const qrCode = await page.waitForSelector('img[alt="QR Code"]');
    expect(qrCode).toBeTruthy();
    
    // Student login (new context)
    const studentPage = await context.newPage();
    await studentPage.goto('/login');
    await studentPage.fill('[name=email]', 'student@stxaviers.edu.in');
    await studentPage.fill('[name=password]', 'StudentPass123!');
    await studentPage.click('button[type=submit]');
    
    // Scan QR (mock camera)
    await studentPage.click('text=Scan Attendance');
    await studentPage.evaluate(() => {
      // Mock QR scanner result
      window.mockQRResult = 'https://educore.in/a/SES_001?tok=abc123';
    });
    
    // Verify attendance marked
    await expect(studentPage.locator('text=Attendance Marked Successfully')).toBeVisible();
    
    // Teacher sees updated count
    await page.waitForSelector('text=Present: 1/60');
  });
});
```

### 4.5 Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_attendance.py -v

# Run E2E tests
npx playwright test

# Run tests in CI mode
pytest -x --cov=app --cov-fail-under=90
```

---

## 5. CI/CD Pipeline

### 5.1 GitHub Actions Workflow

#### .github/workflows/ci.yml
```yaml
name: CI Pipeline

on:
  push:
    branches: [develop, main]
  pull_request:
    branches: [develop]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install black ruff mypy pre-commit
          pre-commit install
      
      - name: Run linters
        run: |
          black --check app/
          ruff check app/
          mypy app/

  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
      
      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov pytest-asyncio
      
      - name: Run tests
        run: |
          pytest --cov=app --cov-report=xml --cov-fail-under=90
        env:
          DATABASE_URL: postgresql+asyncpg://postgres:postgres@localhost:5432/postgres
          REDIS_URL: redis://localhost:6379/0
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml

  build:
    needs: [lint, test]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Build Docker image
        run: docker build -t educore-api:${{ github.sha }} .
      
      - name: Push to registry
        run: |
          echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
          docker push educore-api:${{ github.sha }}

  deploy-staging:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/develop'
    
    steps:
      - name: Deploy to staging
        run: |
          # SSH into staging server and deploy
          ssh -o StrictHostKeyChecking=no ${{ secrets.STAGING_USER }}@${{ secrets.STAGING_HOST }} << 'EOF'
            cd /opt/educore
            docker-compose pull
            docker-compose up -d
          EOF

  deploy-production:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: production
    
    steps:
      - name: Deploy to production
        run: |
          # Blue-green deployment
          ssh -o StrictHostKeyChecking=no ${{ secrets.PROD_USER }}@${{ secrets.PROD_HOST }} << 'EOF'
            cd /opt/educore
            docker-compose pull
            docker-compose up -d --scale api=3
          EOF
```

---

## 6. Deployment Architecture

### 6.1 Docker Compose (Development)

#### docker-compose.yml
```yaml
version: '3.8'

services:
  api:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:password@db:5432/educore
      - REDIS_URL=redis://redis:6379/0
    volumes:
      - ./backend:/app
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started

  web:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
    volumes:
      - ./frontend:/app
      - /app/node_modules
    depends_on:
      - api

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: educore
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

  minio:
    image: minio/minio
    command: server /data --console-address ":9001"
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    volumes:
      - minio_data:/data

volumes:
  postgres_data:
  redis_data:
  minio_data:
```

### 6.2 Production Deployment (Kubernetes)

#### k8s/deployment.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: educore-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: educore-api
  template:
    metadata:
      labels:
        app: educore-api
    spec:
      containers:
      - name: api
        image: educore-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: educore-secrets
              key: database-url
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

---

## 7. Monitoring & Observability

### 7.1 Logging Stack

- **Application Logs**: Structured JSON logs to stdout
- **Log Aggregation**: Loki + Promtail
- **Log Visualization**: Grafana

### 7.2 Metrics Collection

- **Application Metrics**: Prometheus client
- **Metrics Storage**: Prometheus
- **Dashboards**: Grafana
- **Alerting**: Alertmanager

### 7.3 Distributed Tracing

- **Tracing**: OpenTelemetry
- **Backend**: Jaeger or Tempo
- **Sampling Rate**: 10% for production, 100% for staging

### 7.4 Error Tracking

- **Service**: Sentry
- **Environments**: development, staging, production
- **Sample Rate**: 100% errors, 1% performance traces

---

## 8. Security Checklist

### 8.1 Pre-Deployment Security Review

- [ ] All dependencies scanned for vulnerabilities ( Dependabot enabled)
- [ ] OWASP Top 10 vulnerabilities tested
- [ ] SQL injection prevention verified
- [ ] XSS prevention implemented
- [ ] CSRF tokens enabled
- [ ] Rate limiting configured
- [ ] HTTPS enforced (HSTS headers)
- [ ] Security headers set (CSP, X-Frame-Options, etc.)
- [ ] Secrets managed via environment variables (not hardcoded)
- [ ] Database credentials rotated
- [ ] Firewall rules configured
- [ ] Backup strategy tested

### 8.2 Regular Security Audits

- **Monthly**: Dependency vulnerability scan
- **Quarterly**: Penetration testing
- **Bi-annually**: Full security audit by third party
- **Annually**: Compliance audit (ISO 27001, SOC 2)

---

**Document Status**: ✅ Complete  
**Next Step**: Set up CI/CD pipeline and development environments  
**Approval Required**: DevOps lead sign-off before Sprint 1 kickoff
