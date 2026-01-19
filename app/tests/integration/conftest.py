"""
Pytest fixtures for integration tests.

Integration tests use a real test database to test the full stack:
Router → Service → CRUD → Database
"""

import os
import pytest
import psycopg2
from psycopg2 import pool
from app.services.expenses import ExpenseService


@pytest.fixture(scope="session")
def test_database_url():
    """Get test database URL from environment or use default"""
    return os.getenv(
        "TEST_DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/expensetracker_test"
    )


@pytest.fixture(scope="session")
def test_db_pool(test_database_url):
    """Create a connection pool for test database"""
    # Try to create test database if it doesn't exist
    try:
        # Connect to postgres database to create test database
        base_url = test_database_url.rsplit("/", 1)[0] + "/postgres"
        conn = psycopg2.connect(base_url)
        conn.autocommit = True
        cursor = conn.cursor()
        db_name = test_database_url.rsplit("/", 1)[1]
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
        if not cursor.fetchone():
            cursor.execute(f"CREATE DATABASE {db_name}")
        cursor.close()
        conn.close()
    except Exception:
        pass  # Database might already exist or we can't create it

    test_pool = pool.SimpleConnectionPool(minconn=1, maxconn=5, dsn=test_database_url)
    yield test_pool
    test_pool.closeall()


@pytest.fixture(scope="session")
def test_db_schema(test_db_pool):
    """Initialize test database schema"""
    # Get path to schema.sql
    # conftest.py is in app/tests/integration/
    # schema.sql is in app/db/
    # So we need to go up 3 levels: integration -> tests -> app -> root
    current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    schema_path = os.path.join(current_dir, "app", "db", "schema.sql")

    with open(schema_path, "r") as f:
        sql = f.read()

    conn = test_db_pool.getconn()
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
    finally:
        test_db_pool.putconn(conn)


@pytest.fixture
def test_conn(test_db_pool, test_db_schema):
    """Get a test database connection with transaction rollback"""
    conn = test_db_pool.getconn()
    conn.autocommit = False
    try:
        yield conn
    finally:
        conn.rollback()  # Rollback all changes after test
        test_db_pool.putconn(conn)


@pytest.fixture
def expense_service(test_conn):
    """Create ExpenseService with test database connection"""
    return ExpenseService(test_conn)
