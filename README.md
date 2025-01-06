# URL Shortener

A fast and efficient URL shortener service built with FastAPI and SQLAlchemy. Create shortened URLs instantly, with support for custom URLs and comprehensive logging.

## Features

- 🚀 Fast URL shortening with automatic hash generation
- ✨ Custom URL support
- 🔍 Duplicate URL detection
- 🛡️ Input validation and sanitization
- 📝 SQLite database (easily adaptable to PostgreSQL)
- 📚 Auto-generated API documentation
- ⚙️ Environment-based configuration
- 📊 Comprehensive logging system

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/url-shortener.git
cd url-shortener
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create configuration:
```bash
cp .env.example .env
# Edit .env with your preferred settings
```

## Configuration

The application uses environment variables for configuration. Available settings:

### Application Settings
- `APP_NAME`: Name of the application (default: "URL Shortener")
- `APP_VERSION`: Application version (default: "1.0.0")
- `DEBUG`: Debug mode (default: False)

### Database Settings
- `DATABASE_URL`: Database connection string (default: "sqlite:///./shortener.db")

### Logging Settings
- `LOG_LEVEL`: Logging level (default: "INFO")
- `LOG_FORMAT`: Log message format
- `LOG_FILE`: Log file path (optional)

### URL Settings
- `MIN_CUSTOM_URL_LENGTH`: Minimum length for custom URLs (default: 4)
- `MAX_CUSTOM_URL_LENGTH`: Maximum length for custom URLs (default: 30)
- `AUTO_URL_LENGTH`: Length of auto-generated URLs (default: 8)

## Usage

1. Start the server:
```bash
uvicorn main:app --reload
```

2. Access the API documentation at `http://localhost:8000/docs`

### API Endpoints

#### Create Shortened URL
```bash
POST /url

# Request body (with custom URL):
{
    "target_url": "https://example.com",
    "custom_url": "my-link"  # Optional
}

# Response:
{
    "short_url": "my-link",
    "target_url": "https://example.com",
    "is_custom": true,
    "created_at": "2024-01-06T12:00:00"
}
```

#### Access Shortened URL
```bash
GET /{short_url}

# Response:
{
    "url": "https://example.com"
}
```

## Project Structure

```
url-shortener/
├── app/                    # Main application package
│   ├── api/               # API endpoints
│   ├── core/              # Core functionality
│   ├── db/                # Database models
│   ├── schemas/           # Pydantic models
│   └── services/          # Business logic
├── logs/                  # Log files
└── tests/                 # Test suite
```

### Key Components

- `app/core/config.py`: Configuration management using Pydantic settings
- `app/core/logging.py`: Logging setup and utilities
- `app/services/shortener.py`: URL shortening business logic
- `app/api/endpoints.py`: FastAPI route handlers
- `app/db/models.py`: SQLAlchemy database models

## Development

### Running Tests

```bash
pytest tests/
```

### Logging

The application uses a comprehensive logging system that includes:
- Console logging for development
- File logging for production
- Different log levels (DEBUG, INFO, WARNING, ERROR)
- Structured log format with timestamps and context

Log files are stored in the `logs/` directory by default.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Dependencies

- FastAPI: Web framework
- SQLAlchemy: Database ORM
- Pydantic: Data validation
- Python-dotenv: Environment configuration
- Uvicorn: ASGI server

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- FastAPI for the amazing web framework
- SQLAlchemy for the ORM
- All contributors who help improve this project
- Claude 3.5 Sonnet 
