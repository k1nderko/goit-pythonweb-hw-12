"""
FastAPI application for the Contact Management API.

This module sets up the FastAPI application with:
- CORS middleware
- Rate limiting
- API routers for contacts and authentication
- Root endpoint
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from src.api.contacts import router as contacts_router
from src.api.auth import router as auth_router
from src.services.limiter import limiter

app = FastAPI(
    title="Contact Management API",
    description="API for managing contacts with user authentication and rate limiting",
    version="1.0.0"
)

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(contacts_router, prefix="/api/contacts", tags=["contacts"])
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])

@app.get("/")
@limiter.limit("5/minute")
async def read_root(request: Request):
    """
    Root endpoint that returns a welcome message.
    
    Args:
        request: Request - The request object
        
    Returns:
        dict: A welcome message
    """
    return {"message": "Welcome to Contact API"} 