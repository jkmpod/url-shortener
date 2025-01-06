# tests/test_models.py
import pytest
from datetime import datetime
from app.db.models import URL

class TestURLModel:
    """
    Test suite for URL database model.
    
    Demonstrates:
    - Model validation
    - Database operations
    - Field constraints
    - Default values
    
    Example:
        ```python
        def test_custom_model_behavior(db_session):
            url = URL(
                original_url="https://example.com",
                short_url="custom"
            )
            db_session.add(url)
            db_session.commit()
            
            assert url.is_custom is False  # Default value
            assert isinstance(url.created_at, datetime)
        ```
    """
    
    def test_create_url(self, db_session):
        """Test basic URL creation"""
        url = URL(
            original_url="https://example.com",
            short_url="test123",
            is_custom=True
        )
        db_session.add(url)
        db_session.commit()
        
        saved_url = db_session.query(URL).first()
        assert saved_url.original_url == "https://example.com"
        assert saved_url.short_url == "test123"
        assert saved_url.is_custom is True
        assert isinstance(saved_url.created_at, datetime)
    
    def test_url_defaults(self, db_session):
        """Test default values for URL model"""
        url = URL(
            original_url="https://example.com",
            short_url="test123"
        )
        db_session.add(url)
        db_session.commit()
        
        saved_url = db_session.query(URL).first()
        assert saved_url.is_custom is False  # Default value
        assert (datetime.utcnow() - saved_url.created_at).total_seconds() < 5
    
    def test_url_unique_constraint(self, db_session):
        """Test unique constraint on short_url"""
        # Create first URL
        url1 = URL(
            original_url="https://example.com",
            short_url="test123"
        )
        db_session.add(url1)
        db_session.commit()
        
        # Try to create second URL with same short_url
        url2 = URL(
            original_url="https://another-example.com",
            short_url="test123"
        )
        db_session.add(url2)
        
        with pytest.raises(Exception) as excinfo:
            db_session.commit()
        assert "UNIQUE constraint failed" in str(excinfo.value)
    
    def test_url_relationships(self, db_session):
        """
        Test URL model relationships (example for future expansion).
        
        This test demonstrates how to test relationships when you add them
        to the model in the future (e.g., user ownership, click tracking).
        """
        url = URL(
            original_url="https://example.com",
            short_url="test123"
        )
        db_session.add(url)
        db_session.commit()
        
        # Example for future expansion:
        # assert len(url.clicks) == 0  # If you add click tracking
        # assert url.user is None      # If you add user ownership
