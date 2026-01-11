import os
from psycopg2 import pool
from app.config import settings

_pool = None

def init_pool():
    """Initialize the database connection pool"""
    global _pool
    _pool = pool.SimpleConnectionPool(
        minconn=2,
        maxconn=10,
        dsn=settings.database_url
    )

def close_pool():
    """Close the database connection pool"""
    global _pool
    if _pool:
        _pool.closeall()

def get_connection():
    """Get a connection from the pool"""
    if _pool is None:
        raise Exception("Database connection pool not initialized")
    conn = _pool.getconn()
    try:
        yield conn
    finally:
        _pool.putconn(conn)

def init_db():
    """Execute schema.sql to create tables"""
    current_dir = os.path.dirname(__file__)
    schema_path = os.path.join(current_dir, 'db', 'schema.sql')
    
    with open(schema_path, 'r') as f:
        sql = f.read()
    
    conn = _pool.getconn()
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        print("✅ Database initialized successfully")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error initializing database: {e}")
        raise
    finally:
        _pool.putconn(conn)


