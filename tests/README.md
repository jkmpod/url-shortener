# Testing Guide - URL Shortener

## Table of Contents
- [Testing Structure](#testing-structure)
- [Test Categories](#test-categories)
- [Testing Principles](#testing-principles)
- [Best Practices](#best-practices)
- [Running Tests](#running-tests)
- [Test Coverage](#test-coverage)
- [Troubleshooting](#troubleshooting)

## Testing Structure

```
tests/
├── __init__.py
├── conftest.py               # Shared fixtures and configuration
├── test_api.py              # API integration tests
├── test_shortener.py        # Unit tests for core functionality
└── test_models.py           # Database model tests
```

### File Organization Principles

1. **conftest.py**
   - Global test configuration
   - Shared fixtures
   - Database setup/teardown
   - Test client setup

2. **test_api.py**
   - API endpoint testing
   - Request/response validation
   - Error handling
   - Integration scenarios

3. **test_shortener.py**
   - Core business logic
   - URL validation
   - Hash generation
   - Edge cases

## Test Categories

### 1. Unit Tests
Focus on testing individual components in isolation.

```python
# Example unit test
def test_url_validation():
    assert validate_custom_url("valid-url") == True
    assert validate_custom_url("-invalid") == False
```

### 2. Integration Tests
Test multiple components working together.

```python
# Example integration test
def test_url_creation_flow(client, db_session):
    # Test entire flow from API to database
    response = client.post("/url", json={"target_url": "https://example.com"})
    assert response.status_code == 200
    
    # Verify database entry
    url = db_session.query(URL).first()
    assert url.original_url == "https://example.com"
```

### 3. Functional Tests
Test complete features from a user's perspective.

```python
# Example functional test
def test_url_shortening_feature(client):
    # Create short URL
    create_response = client.post("/url", json={
        "target_url": "https://example.com"
    })
    short_url = create_response.json()["short_url"]
    
    # Verify retrieval
    get_response = client.get(f"/{short_url}")
    assert get_response.json()["url"] == "https://example.com"
```

## Testing Principles

### 1. AAA Pattern
Follow the Arrange-Act-Assert pattern:

```python
def test_example():
    # Arrange
    url_data = {"target_url": "https://example.com"}
    
    # Act
    response = client.post("/url", json=url_data)
    
    # Assert
    assert response.status_code == 200
    assert response.json()["target_url"] == url_data["target_url"]
```

### 2. Test Isolation
Each test should:
- Be independent
- Clean up after itself
- Not rely on other tests
- Use fresh fixtures

### 3. Meaningful Names
Use descriptive test names that indicate:
- What is being tested
- Under what conditions
- Expected outcome

```python
def test_custom_url_creation_fails_when_url_already_exists():
    # Test content
```

## Best Practices

### 1. Fixture Usage

```python
# Bad: Hard-coded test data
def test_bad():
    url = "https://example.com"
    
# Good: Use fixtures
def test_good(valid_url_data):
    response = create_url(valid_url_data)
```

### 2. Error Testing

```python
# Test both success and error cases
def test_error_handling(client):
    response = client.post("/url", json={
        "target_url": "invalid-url"
    })
    assert response.status_code == 422
    assert "invalid" in response.json()["detail"].lower()
```

### 3. Parameterized Testing

```python
@pytest.mark.parametrize("url,expected_status", [
    ("https://example.com", 200),
    ("invalid-url", 422),
    ("", 422),
])
def test_url_validation(client, url, expected_status):
    response = client.post("/url", json={"target_url": url})
    assert response.status_code == expected_status
```

## Running Tests

### Basic Test Run
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_api.py

# Run specific test
pytest tests/test_api.py::test_create_url
```

### Test Options
```bash
# Run with coverage
pytest --cov=app tests/

# Run with verbose output
pytest -v

# Run tests matching pattern
pytest -k "create or custom"
```

## Test Coverage

### Coverage Goals
- Aim for 80%+ coverage
- Focus on critical paths
- Don't chase 100% blindly

### Coverage Report
```bash
# Generate coverage report
pytest --cov=app --cov-report=term-missing tests/

# Generate HTML report
pytest --cov=app --cov-report=html tests/
```

## Troubleshooting

### Common Issues

1. **Database State Issues**
   - Use `db_session` fixture
   - Ensure proper cleanup
   - Check transaction isolation

2. **Fixture Errors**
   - Check fixture dependencies
   - Verify scope (function/session)
   - Look for cleanup issues

3. **Async Test Issues**
   - Use `async def` for async tests
   - Use proper async fixtures
   - Handle coroutines correctly

### Debug Tips

1. Use pytest's built-in debugger:
```bash
pytest --pdb
```

2. Print debugging information:
```python
def test_with_debug(caplog):
    caplog.set_level(logging.DEBUG)
    # Your test code
```

3. Use pytest's verbose mode:
```bash
pytest -v --showlocals
```

## Contributing Tests

When adding new tests:
1. Follow existing patterns
2. Add appropriate docstrings
3. Include example usage
4. Update this documentation
5. Maintain test categories
