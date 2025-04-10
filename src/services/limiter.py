"""
Rate limiting service for the API.

This module provides rate limiting functionality using slowapi.
It includes different rate limits for testing and production environments.
"""

from slowapi import Limiter
from slowapi.util import get_remote_address
from src.conf.config import settings

def get_request_key(request):
    """
    Get a key for rate limiting based on the request.
    
    In testing mode, returns a fixed key "test".
    In production mode, returns the client's IP address.
    
    Args:
        request: Request - The FastAPI request object
        
    Returns:
        str: The key to use for rate limiting
    """
    if settings.TESTING:
        return "test"
    return get_remote_address(request)

# Use a much higher rate limit during tests
if settings.TESTING:
    limiter = Limiter(key_func=get_request_key, default_limits=["1000/minute"])
    # Override the storage to use a shorter time window for testing
    def reset_limiter():
        """
        Reset the rate limiter storage.
        
        This function is used in tests to reset the rate limiter
        between test cases.
        """
        limiter._storage.reset()
    limiter.reset = reset_limiter
else:
    limiter = Limiter(key_func=get_request_key, default_limits=["5/minute"])
