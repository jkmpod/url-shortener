# tests/test_api.py
import pytest
from fastapi import status
from app.core.config import get_settings

settings = get_settings()

class TestURLShortener:
    """
    Test suite for URL shortener API endpoints.
    
    This test class uses several fixtures defined in conftest.py:
    - client: FastAPI TestClient instance
    - valid_url_data: Dictionary with valid URL data
    - valid_long_url_data: Dictionary with valid long URL
    
    Example usage:
        ```python
        class TestURLShortener:
            def test_custom_functionality(self, client, valid_url_data):
                # Example showing how to use fixtures in a test
                
                # First, create a URL using valid_url_data
                create_response = client.post("/url", json=valid_url_data)
                assert create_response.status_code == status.HTTP_200_OK
                
                # Then test retrieving it
                short_url = create_response.json()["short_url"]
                get_response = client.get(f"/{short_url}")
                assert get_response.status_code == status.HTTP_200_OK
        ```
    """
    
    def test_create_url(self, client, valid_url_data):
        """
        Test creating a shortened URL with a custom code.
        
        This test demonstrates:
        1. Using the client fixture to make API requests
        2. Using valid_url_data fixture for test data
        3. Validating the response structure
        
        Example:
            ```python
            def test_similar_case(self, client, valid_url_data):
                # You can modify the fixture data for your specific test
                modified_data = {
                    **valid_url_data,
                    "custom_url": "my-custom-url"
                }
                response = client.post("/url", json=modified_data)
                assert response.status_code == status.HTTP_200_OK
            ```
        """
        response = client.post("/url", json=valid_url_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["target_url"] == valid_url_data["target_url"]
        assert data["short_url"] == valid_url_data["custom_url"]
        assert data["is_custom"] is True
    
    def test_create_url_auto_generated(self, client, valid_long_url_data):
        """
        Test creating a URL with auto-generated short code.
        
        This test demonstrates:
        1. Using valid_long_url_data fixture for auto-generation testing
        2. Validating the auto-generated URL length
        3. Checking the is_custom flag
        
        Example:
            ```python
            def test_another_auto_case(self, client, valid_long_url_data):
                # You can add additional URLs to test consistency
                first_response = client.post("/url", json=valid_long_url_data)
                second_response = client.post("/url", json=valid_long_url_data)
                
                # Same URL should get same short code
                assert first_response.json()["short_url"] == second_response.json()["short_url"]
            ```
        """
        response = client.post("/url", json=valid_long_url_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["target_url"] == valid_long_url_data["target_url"]
        assert len(data["short_url"]) == settings.AUTO_URL_LENGTH
        assert data["is_custom"] is False
    
    def test_create_duplicate_custom_url(self, client, valid_url_data):
        """
        Test handling of duplicate custom URLs.
        
        This test demonstrates:
        1. Creating multiple URLs with the same custom code
        2. Handling error responses
        3. Validating error messages
        
        Example:
            ```python
            def test_similar_duplicate_case(self, client, valid_url_data):
                # First create a URL
                first = client.post("/url", json=valid_url_data)
                
                # Try different variations of the same custom URL
                variations = [
                    valid_url_data["custom_url"].upper(),
                    f"-{valid_url_data['custom_url']}-"
                ]
                
                for variant in variations:
                    duplicate_data = {
                        **valid_url_data,
                        "custom_url": variant
                    }
                    response = client.post("/url", json=duplicate_data)
                    assert response.status_code == status.HTTP_400_BAD_REQUEST
            ```
        """
        # Create first URL
        response1 = client.post("/url", json=valid_url_data)
        assert response1.status_code == status.HTTP_200_OK
        
        # Try to create second URL with same custom code
        duplicate_data = {
            "target_url": "https://another-example.com",
            "custom_url": valid_url_data["custom_url"]
        }
        response2 = client.post("/url", json=duplicate_data)
        assert response2.status_code == status.HTTP_400_BAD_REQUEST
        assert "already taken" in response2.json()["detail"].lower()

    # ... [Previous test methods remain the same] ...

    @pytest.mark.parametrize("custom_url", [
        pytest.param("a" * 31, id="too-long"),
        pytest.param("ab", id="too-short"),
        pytest.param("-invalid", id="starts-with-hyphen"),
        pytest.param("invalid-", id="ends-with-hyphen"),
        pytest.param("in val", id="contains-space"),
        pytest.param("admin", id="reserved-word")
    ])
    def test_invalid_custom_urls(self, client, custom_url):
        """
        Test various invalid custom URL formats using parameterization.
        
        This test demonstrates:
        1. Using pytest.mark.parametrize for multiple test cases
        2. Testing different invalid URL formats
        3. Identifying test cases with descriptive IDs
        
        Example:
            ```python
            @pytest.mark.parametrize("custom_url,expected_error", [
                ("short", "URL too short"),
                ("very-very-long-url", "URL too long"),
            ])
            def test_custom_validations(self, client, custom_url, expected_error):
                data = {
                    "target_url": "https://example.com",
                    "custom_url": custom_url
                }
                response = client.post("/url", json=data)
                assert response.status_code == status.HTTP_400_BAD_REQUEST
                assert expected_error in response.json()["detail"]
            ```
        """
        data = {
            "target_url": "https://example.com",
            "custom_url": custom_url
        }
        response = client.post("/url", json=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
