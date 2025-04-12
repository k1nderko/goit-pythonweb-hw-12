"""
Application Configuration Module

This module defines the application settings using Pydantic's BaseSettings.
It loads configuration from environment variables and provides default values
for all required settings.

The settings include:
- Database configuration
- Authentication settings
- Email settings
- Cloudinary settings
- Redis settings
- Testing mode
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import os

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    This class defines all configuration parameters for the application,
    with default values that can be overridden by environment variables.
    """
    DATABASE_URL: str = "sqlite:///./test.db"
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Mail settings
    MAIL_USERNAME: str = "test@example.com"
    MAIL_PASSWORD: str = "test_password"
    MAIL_FROM: str = "test@example.com"
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.gmail.com"
    
    # Cloudinary settings
    CLOUDINARY_NAME: str = "your-cloud-name"
    CLOUDINARY_API_KEY: str = "your-api-key"
    CLOUDINARY_API_SECRET: str = "your-api-secret"
    
    # Redis settings
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_user_cache_ttl: int = 3600
    
    # Test mode
    TESTING: bool = os.getenv("TESTING", "False").lower() == "true"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

@lru_cache()
def get_settings():
    """
    Get application settings with caching.
    
    This function uses lru_cache to avoid reloading settings on each call,
    improving performance.
    
    Returns:
        Settings: The application settings instance
    """
    return Settings()

settings = get_settings()
