# conftest.py
import os
import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from main import app
from app.database import Base
from app.dependencies import get_db
# Base Postgres connection (to the admin DB) – never your prod DB string directly
PG_ADMIN_URL = os.getenv(
    "PG_ADMIN_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres",
)

# Create a unique test DB name so parallel runs don’t collide
TEST_DB_NAME = f"test_db_{uuid.uuid4().hex[:8]}"

# 1) Create the throwaway test database
AdminEngine = create_engine(PG_ADMIN_URL, isolation_level="AUTOCOMMIT", future=True)
with AdminEngine.connect() as conn:
    conn.execute(text(f'CREATE DATABASE "{TEST_DB_NAME}"'))

# 2) Build engine/session to the new test DB
TEST_DATABASE_URL = PG_ADMIN_URL.rsplit("/", 1)[0] + f"/{TEST_DB_NAME}"
TestEngine = create_engine(TEST_DATABASE_URL, future=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=TestEngine)

# 3) Create schema on the test DB
Base.metadata.create_all(bind=TestEngine)

def override_get_db():
    """Use the test DB session during testing."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Make app use the test DB
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def test_client():
    client = TestClient(app)
    yield client
    # 4) Tear down: drop all tables (optional) and drop the whole DB
    TestEngine.dispose()
    with AdminEngine.connect() as conn:
        # Kick out any lingering connections and drop
        conn.execute(text(f"""
            SELECT pg_terminate_backend(pid)
            FROM pg_stat_activity
            WHERE datname = :db AND pid <> pg_backend_pid();
        """), {"db": TEST_DB_NAME})
        conn.execute(text(f'DROP DATABASE "{TEST_DB_NAME}"'))
    AdminEngine.dispose()
