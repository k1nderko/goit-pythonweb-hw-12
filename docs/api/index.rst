API Documentation
===============

This section provides detailed documentation for the REST API endpoints.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   auth
   contacts

Overview
--------

The API provides endpoints for user authentication and contact management. All endpoints are prefixed with ``/api``.

Authentication
-------------

Most endpoints require authentication using a JWT token. To authenticate:

1. Register a new user using the ``/api/auth/register`` endpoint
2. Verify your email using the link sent to your email address
3. Login using the ``/api/auth/login`` endpoint to get an access token
4. Include the access token in the Authorization header of subsequent requests:

   .. sourcecode:: text

      Authorization: Bearer <your_access_token>

Rate Limiting
------------

The API implements rate limiting to prevent abuse:

- Authentication endpoints: 5 requests per minute
- Contact endpoints: 5 requests per minute
- Search endpoint: 5 requests per minute

In testing mode, the rate limits are increased to 100 requests per minute.

Error Responses
-------------

The API uses standard HTTP status codes and returns error messages in the following format:

.. sourcecode:: json

   {
     "detail": "Error message description"
   }

Common error codes:

- 400: Bad Request - Invalid input data
- 401: Unauthorized - Missing or invalid authentication
- 403: Forbidden - Insufficient permissions
- 404: Not Found - Resource not found
- 409: Conflict - Resource already exists
- 429: Too Many Requests - Rate limit exceeded
- 500: Internal Server Error - Server error 