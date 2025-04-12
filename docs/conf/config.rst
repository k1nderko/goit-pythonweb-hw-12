Configuration Module
==================

The configuration module provides application settings using Pydantic's BaseSettings.

Settings Class
------------

.. automodule:: src.conf.config
   :members:
   :undoc-members:
   :show-inheritance:

Environment Variables
-------------------

The application uses the following environment variables:

.. list-table::
   :header-rows: 1

   * - Variable
     - Description
     - Default
   * - DATABASE_URL
     - PostgreSQL connection string
     - sqlite:///./test.db
   * - SECRET_KEY
     - Secret key for JWT token generation
     - your-secret-key
   * - ALGORITHM
     - Algorithm for JWT token generation
     - HS256
   * - ACCESS_TOKEN_EXPIRE_MINUTES
     - Access token expiration time in minutes
     - 30
   * - REFRESH_TOKEN_EXPIRE_DAYS
     - Refresh token expiration time in days
     - 7
   * - MAIL_USERNAME
     - Email username for sending emails
     - test@example.com
   * - MAIL_PASSWORD
     - Email password for sending emails
     - test_password
   * - MAIL_FROM
     - Sender email address
     - test@example.com
   * - MAIL_PORT
     - SMTP server port
     - 587
   * - MAIL_SERVER
     - SMTP server address
     - smtp.gmail.com
   * - CLOUDINARY_NAME
     - Cloudinary cloud name
     - your-cloud-name
   * - CLOUDINARY_API_KEY
     - Cloudinary API key
     - your-api-key
   * - CLOUDINARY_API_SECRET
     - Cloudinary API secret
     - your-api-secret
   * - REDIS_HOST
     - Redis server host
     - localhost
   * - REDIS_PORT
     - Redis server port
     - 6379
   * - REDIS_DB
     - Redis database number
     - 0
   * - REDIS_USER_CACHE_TTL
     - User cache TTL in seconds
     - 3600
   * - TESTING
     - Testing mode flag
     - False 