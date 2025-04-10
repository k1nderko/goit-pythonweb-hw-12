# Contact Management API

A FastAPI-based REST API for managing contacts with authentication and rate limiting.

## Features

- User authentication with JWT tokens
- Contact management (CRUD operations)
- Rate limiting
- PostgreSQL database
- Alembic migrations
- Pytest test suite

## Installation

```bash
# Install dependencies
poetry install

# Run migrations
alembic upgrade head

# Start the server
uvicorn main:app --reload
```

## Testing

```bash
pytest -v
``` 