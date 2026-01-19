# Expense Tracker - Project Summary

## Overview
RESTful API для отслеживания расходов на FastAPI + PostgreSQL. Проект использует layered architecture с четким разделением ответственности.

## Tech Stack
- **Framework**: FastAPI (Python 3.11)
- **Database**: PostgreSQL 15
- **ORM/Driver**: psycopg2 (raw SQL, не SQLAlchemy ORM)
- **Validation**: Pydantic v2
- **Testing**: pytest, pytest-mock, pytest-cov
- **Containerization**: Docker + docker-compose
- **CI/CD**: GitHub Actions

## Architecture (Layered)
```
Routers (FastAPI endpoints) 
  ↓ Depends on
Services (Business logic, error handling)
  ↓ Depends on
CRUD (Database operations, raw SQL)
  ↓ Uses
Database (PostgreSQL via psycopg2 connection pool)
```

## Project Structure
```
app/
├── app.py              # FastAPI app, lifespan events, router registration
├── config.py           # Pydantic Settings (database_url from env)
├── database.py         # Connection pool (SimpleConnectionPool), init_db()
├── dependencies.py      # FastAPI dependency: get_expense_service()
├── models/             # Pydantic models (ExpenseCreate, ExpenseResponse, ExpenseUpdate)
├── routers/            # FastAPI routes (expenses.py - CRUD endpoints)
├── services/           # Business logic (ExpenseService, DatabaseError)
├── crud/               # Database operations (raw SQL with psycopg2)
└── tests/
    ├── unit/           # Unit tests with mocks (mock_conn, mock_cursor)
    └── integration/    # Integration tests with real DB (test_db_pool fixture)
```

## Data Model
**Table: expenses**
- `id` (SERIAL PRIMARY KEY)
- `amount` (NUMERIC(10,2)) - Decimal для точности денег
- `category` (VARCHAR(100))
- `description` (VARCHAR(255), nullable)
- `date` (DATE)
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)
- Indexes: date, category

**Pydantic Models:**
- `ExpenseCreate`: amount, category, description, date (all required)
- `ExpenseResponse`: + id, created_at, updated_at
- `ExpenseUpdate`: все поля Optional (partial updates)

## API Endpoints
- `POST /expenses/` - Create expense (201)
- `GET /expenses/` - List all (200, ordered by date DESC)
- `GET /expenses/{id}` - Get by ID (200/404)
- `PUT /expenses/{id}` - Update expense (200/404, partial updates supported)
- `DELETE /expenses/{id}` - Delete expense (204/404)
- `GET /` - Health check
- `GET /health` - Health check

## Key Implementation Details

### Database Connection
- **Connection Pool**: `psycopg2.SimpleConnectionPool` (minconn=2, maxconn=10)
- **Pool Management**: Initialized in `lifespan` event, closed on shutdown
- **Connection Injection**: FastAPI dependency `get_connection()` yields connection from pool
- **Schema**: Loaded from `app/db/schema.sql` on startup via `init_db()`

### Dependency Injection Flow
1. Router endpoint calls `Depends(get_expense_service)`
2. `get_expense_service()` calls `Depends(get_connection)`
3. `get_connection()` yields connection from pool
4. `ExpenseService` wraps connection and calls CRUD functions
5. Connection returned to pool after request

### Error Handling
- **Service Layer**: Catches `psycopg2.Error`, wraps in `DatabaseError`
- **Router Layer**: Catches `DatabaseError`, returns HTTP 500
- **CRUD Layer**: Manual rollback on errors, commit on success
- **Validation**: Pydantic validates request models (amount > 0, date not future, etc.)

### Testing Strategy
- **Unit Tests**: Mock database connections (`mock_conn`, `mock_cursor` fixtures)
- **Integration Tests**: Real PostgreSQL via `test_db_pool` fixture, transactions rolled back
- **CI**: PostgreSQL service in GitHub Actions, `DATABASE_URL` env var required

## Configuration
- **Environment Variable**: `DATABASE_URL` (required by `Settings` in config.py)
- **Format**: `postgresql://user:password@host:port/database`
- **Test Database**: `TEST_DATABASE_URL` used only in integration test fixtures

## Important Patterns
- **Raw SQL**: No ORM, direct psycopg2 usage for learning
- **Context Managers**: `with conn.cursor() as cursor:` for cursor management
- **Transaction Management**: Manual commit/rollback in CRUD layer
- **Partial Updates**: Dynamic SQL building in `update_expense()` based on provided fields
- **Decimal for Money**: Never float, always Decimal for financial amounts

## CI/CD
- GitHub Actions workflow runs on push/PR
- Steps: format check (black), lint (flake8), unit tests, integration tests, coverage
- PostgreSQL service container for integration tests
- `DATABASE_URL` set at job level for all steps
