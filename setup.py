from setuptools import setup, find_packages

setup(
    name="url-shortener",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "validators",
        "python-dotenv",
        "pydantic",
        "pydantic-settings",
        "python-multipart",
        "jinja2",
        "aiofiles",
        "pytest",
        "pytest-asyncio",
        "httpx",
        "pytest-cov",
    ],
)