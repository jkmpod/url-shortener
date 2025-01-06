# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import get_settings
from app.db.base import Base, get_db
from app.main import app
from typing import Generator

settings = get_settings()

# Use in-memory SQLite for testing
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def test_db():
    """
    Creates a clean test database for the test session.
    
    This fixture is session-scoped, meaning it will be created once for the entire
    test session and then destroyed at the end. It creates all database tables
    before tests run and drops them after all tests are complete.
    
    Example:
        ```python
        def test_database_operation(test_db):
            # Database tables are created and ready to use
            # Your test code here
            pass
        ```
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(test_db) -> Generator:
    """
    Provides a clean database session for each test function.
    
    This fixture creates a new database transaction for each test, and rolls it
    back after the test completes. This ensures that each test runs in isolation.
    
    Example:
        ```python
        def test_create_url(db_session):
            # Create a new URL entry
            url = URL(
                original_url="https://example.com",
                short_url="test123"
            )
            db_session.add(url)
            db_session.commit()
            
            # Verify the entry
            saved_url = db_session.query(URL).first()
            assert saved_url.short_url == "test123"
        ```
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session) -> Generator:
    """
    Provides a FastAPI TestClient instance with a clean database session.
    
    This fixture combines the FastAPI test client with a database session,
    allowing you to test API endpoints with database interactions.
    
    Example:
        ```python
        def test_api_endpoint(client):
            # Make a request to your API
            response = client.post(
                "/url",
                json={
                    "target_url": "https://example.com",
                    "custom_url": "test123"
                }
            )
            assert response.status_code == 200
            assert response.json()["short_url"] == "test123"
        ```
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
            
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def valid_url_data():
    """
    Provides a dictionary with valid URL data for testing.
    
    This fixture returns a dictionary containing a valid target URL and custom URL
    that can be used for testing URL creation endpoints.
    
    Example:
        ```python
        def test_create_custom_url(client, valid_url_data):
            # Use the valid_url_data fixture directly
            response = client.post("/url", json=valid_url_data)
            assert response.status_code == 200
            
            # Or modify it for specific test cases
            modified_data = {
                **valid_url_data,
                "custom_url": "different-url"
            }
            response = client.post("/url", json=modified_data)
            assert response.status_code == 200
        ```
    """
    return {
        "target_url": "https://example.com",
        "custom_url": "test-url"
    }

@pytest.fixture
def valid_long_url_data():
    """
    Provides a dictionary with a valid long URL for testing auto-shortening.
    
    This fixture returns a dictionary containing a valid target URL without a
    custom URL, useful for testing the automatic URL shortening functionality.
    
    Example:
        ```python
        def test_auto_url_generation(client, valid_long_url_data):
            # Test automatic short URL generation
            response = client.post("/url", json=valid_long_url_data)
            assert response.status_code == 200
            assert len(response.json()["short_url"]) == settings.AUTO_URL_LENGTH
            
            # You can also combine it with other test data
            custom_data = {
                **valid_long_url_data,
                "custom_url": "custom-code"
            }
            response = client.post("/url", json=custom_data)
            assert response.status_code == 200
        ```
    """
    return {
        "target_url": "https://example.com/very/long/path/to/test"
    }
