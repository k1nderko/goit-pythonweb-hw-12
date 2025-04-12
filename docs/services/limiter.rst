Rate Limiter Service
==================

This module provides rate limiting functionality using Redis.

Rate Limiter
----------

.. automodule:: src.services.limiter
   :members: RateLimiter
   :undoc-members:
   :show-inheritance:

The RateLimiter class provides the following operations:

Check Rate Limit
-------------

.. automodule:: src.services.limiter
   :members: RateLimiter.check_rate_limit
   :undoc-members:
   :show-inheritance:

Checks if a request is within rate limits.

Reset Rate Limit
-------------

.. automodule:: src.services.limiter
   :members: RateLimiter.reset_rate_limit
   :undoc-members:
   :show-inheritance:

Resets the rate limit counter.

Configuration
-----------

The rate limiter is configured with the following settings:

.. list-table::
   :header-rows: 1

   * - Setting
     - Value
     - Description
   * - REDIS_HOST
     - From environment
     - Redis server host
   * - REDIS_PORT
     - From environment
     - Redis server port
   * - REDIS_DB
     - From environment
     - Redis database number
   * - TESTING
     - From environment
     - Testing mode flag

Rate Limits
---------

The following rate limits are enforced:

.. list-table::
   :header-rows: 1

   * - Endpoint
     - Limit
     - Description
   * - /api/auth/*
     - 5/minute
     - Authentication endpoints
   * - /api/contacts/*
     - 5/minute
     - Contact endpoints
   * - /api/contacts/search
     - 5/minute
     - Search endpoint
   * - /*
     - 5/minute
     - Root endpoint

In testing mode, all limits are increased to 1000 requests per minute.

Parameters
---------

.. list-table::
   :header-rows: 1

   * - Parameter
     - Type
     - Description
   * - key
     - str
     - Rate limit key
   * - limit
     - int
     - Maximum requests
   * - period
     - int
     - Time period in seconds

Return Values
-----------

.. list-table::
   :header-rows: 1

   * - Method
     - Return Type
     - Description
   * - check_rate_limit
     - bool
     - True if within limits
   * - reset_rate_limit
     - None
     - No return value 