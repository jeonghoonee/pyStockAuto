"""
Test Configuration

Test configuration and fixtures for PyStockAuto.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.models import Base
from app.config.database import get_db

# Test database URL (use SQLite for testing)
TEST_DATABASE_URL = "sqlite:///./test.db"

# Create test engine
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Create test session
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)

def override_get_db():
    """Override database dependency for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Override the dependency
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
def test_client():
    """Create test client"""
    # Create test database tables
    Base.metadata.create_all(bind=test_engine)
    
    with TestClient(app) as client:
        yield client
    
    # Drop test database tables
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture
def test_db():
    """Create test database session"""
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=test_engine)
