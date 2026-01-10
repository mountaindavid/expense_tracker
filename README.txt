================================================================================
                        EXPENSE TRACKER - LEARNING PROJECT
================================================================================

🎯 PROJECT OVERVIEW & LEARNING GOALS
================================================================================

This is a learning project to master fundamental software development concepts
through building a practical Expense Tracker application.

LEARNING OBJECTIVES:
-------------------
✓ FastAPI framework - Modern Python web framework
✓ PostgreSQL - Relational database management
✓ CRUD operations - Create, Read, Update, Delete
✓ Docker & Containerization - Consistent development environment
✓ RESTful API design - Industry-standard API patterns
✓ SQLAlchemy ORM - Database abstraction layer
✓ Software architecture - Layered architecture patterns


📐 RECOMMENDED ARCHITECTURE
================================================================================

LAYERED ARCHITECTURE (Keep it Simple):

┌─────────────────────────────┐
│   API Layer (FastAPI)       │  ← Routes, request/response models
├─────────────────────────────┤
│   Business Logic Layer      │  ← Service functions, validation
├─────────────────────────────┤
│   Data Access Layer         │  ← Database models, queries
├─────────────────────────────┤
│   Database (PostgreSQL)     │  ← Persistent storage
└─────────────────────────────┘


📁 PROJECT STRUCTURE
================================================================================

ExpenseTracker/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Configuration (DB URL, env vars)
│   ├── database.py          # Database connection & session
│   │
│   ├── models/              # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   └── expense.py
│   │
│   ├── schemas/             # Pydantic models (request/response)
│   │   ├── __init__.py
│   │   └── expense.py
│   │
│   ├── routers/             # API endpoints
│   │   ├── __init__.py
│   │   └── expenses.py
│   │
│   └── services/            # Business logic (optional for now)
│       ├── __init__.py
│       └── expense_service.py
│
├── docker-compose.yml       # Multi-container orchestration
├── Dockerfile              # Python app container
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (gitignored!)
├── .gitignore
└── README.txt


🗂️ DATA MODEL DESIGN
================================================================================

EXPENSE ENTITY:
--------------
- id           : Primary key (auto-generated)
- amount       : Decimal (not float! Money needs precision)
- category     : String (e.g., "Food", "Transport", "Entertainment")
- description  : Optional text
- date         : Date of expense
- created_at   : Timestamp (audit trail)
- updated_at   : Timestamp (audit trail)

DESIGN DECISIONS:
----------------
1. Categories: Start with hardcoded enum (can move to separate table later)
2. Authentication: Start without it (add later)
3. Currency: Single currency for simplicity (USD assumed)


🛠️ TECHNOLOGY STACK
================================================================================

CORE DEPENDENCIES:
-----------------
- fastapi[standard]    # Web framework + uvicorn server
- sqlalchemy           # ORM for database
- psycopg2-binary      # PostgreSQL adapter
- pydantic-settings    # Configuration management

FUTURE ADDITIONS:
----------------
- alembic              # Database migrations (Phase 5)
- pytest               # Unit testing (Phase 5)


🚀 DEVELOPMENT ROADMAP
================================================================================

PHASE 1: FOUNDATION ✓
---------------------
1. Setup requirements.txt
2. Create Dockerfile
3. Setup docker-compose.yml
4. Create app/config.py
5. Create app/database.py

PHASE 2: DATA LAYER
-------------------
6. Define app/models/expense.py (SQLAlchemy ORM model)
7. Test database connection

PHASE 3: API LAYER
------------------
8. Define app/schemas/expense.py (Pydantic request/response models)
9. Create app/routers/expenses.py (CRUD endpoints)
10. Wire up app/main.py (FastAPI app initialization)

PHASE 4: CRUD IMPLEMENTATION
----------------------------
11. POST /expenses - Create expense
12. GET /expenses - List all expenses
13. GET /expenses/{id} - Get single expense
14. PUT /expenses/{id} - Update expense
15. DELETE /expenses/{id} - Delete expense

PHASE 5: ENHANCEMENTS
---------------------
- Add filtering (by date range, category)
- Add aggregation endpoints (total by category, monthly summaries)
- Add database migrations with Alembic
- Add input validation and error handling
- Add unit tests


💡 KEY CONCEPTS TO LEARN
================================================================================

FASTAPI PATTERNS:
----------------
- Dependency injection (for database sessions)
- Path parameters vs query parameters
- Request/response models with Pydantic
- Automatic API documentation (Swagger UI at /docs)

SQLALCHEMY:
----------
- Declarative models vs Core
- Session management (context managers)
- Queries and filtering
- Relationships (for future features)

DOCKER BEST PRACTICES:
---------------------
- Multi-stage builds (optimization)
- Environment variables for config
- Volume mounting for development
- Container networking
- Health checks

API DESIGN:
----------
- RESTful conventions
- HTTP status codes (200, 201, 404, 422, etc.)
- Idempotency
- Error response structure


⚠️ COMMON PITFALLS TO AVOID
================================================================================

1. Using float for money
   → Use Decimal or store as cents (integer)

2. No database session management
   → Use dependency injection

3. Hardcoded credentials
   → Use environment variables

4. No error handling
   → Catch exceptions, return proper status codes

5. No data validation
   → Pydantic handles this, but define constraints

6. Exposing internal IDs
   → OK for learning, but consider UUIDs in production


🐳 DOCKER SETUP
================================================================================

CONNECTION STRING PATTERN:
-------------------------
postgresql://USER:PASSWORD@HOST:PORT/DATABASE

In docker-compose context:
postgresql://expenseuser:yourpassword@db:5432/expensedb

Note: @db:5432 - 'db' is the service name in docker-compose!

RUNNING THE PROJECT:
-------------------
1. docker-compose up --build    # Build and start all containers
2. docker-compose down           # Stop all containers
3. docker-compose logs -f app    # View app logs
4. docker-compose logs -f db     # View database logs


📚 API ENDPOINTS (Planned)
================================================================================

POST   /expenses          - Create new expense
GET    /expenses          - List all expenses
GET    /expenses/{id}     - Get specific expense
PUT    /expenses/{id}     - Update expense
DELETE /expenses/{id}     - Delete expense

Future endpoints:
GET    /expenses/summary            - Get spending summary
GET    /expenses/by-category        - Aggregate by category
GET    /expenses?start_date=...     - Filter by date range


🎓 LEARNING RESOURCES
================================================================================

- FastAPI Documentation: https://fastapi.tiangolo.com/
- SQLAlchemy Documentation: https://docs.sqlalchemy.org/
- PostgreSQL Documentation: https://www.postgresql.org/docs/
- Docker Documentation: https://docs.docker.com/


================================================================================
                            CURRENT STATUS: Phase 1
================================================================================
