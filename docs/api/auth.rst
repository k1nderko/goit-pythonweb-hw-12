Authentication API
=================

All authenticated endpoints require a Bearer token in the Authorization header:

.. sourcecode:: http

   Authorization: Bearer <access_token>

Registration
-----------

.. http:post:: /api/auth/register

   Register a new user.

   **Request Headers:**

   - ``Content-Type: application/json``

   **Request body:**

   .. sourcecode:: json

      {
        "email": "user@example.com",
        "password": "password123",
        "full_name": "John Doe"
      }

   **Validation Rules:**

   - ``email``: Valid email format
   - ``password``: Minimum 8 characters
   - ``full_name``: Required, non-empty string

   **Response:**

   .. sourcecode:: json

      {
        "message": "User registered successfully. Please check your email for verification."
      }

   **Error Response:**

   .. sourcecode:: json

      {
        "detail": "Email already registered"
      }

   :statuscode 201: User registered successfully
   :statuscode 400: Invalid input data
   :statuscode 409: Email already registered
   :statuscode 429: Too many requests

Login
-----

.. http:post:: /api/auth/login

   Login with email and password.

   **Request Headers:**

   - ``Content-Type: application/json``

   **Request body:**

   .. sourcecode:: json

      {
        "username": "user@example.com",
        "password": "password123"
      }

   **Response:**

   .. sourcecode:: json

      {
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "token_type": "bearer"
      }

   **Error Response:**

   .. sourcecode:: json

      {
        "detail": "Invalid credentials"
      }

   :statuscode 200: Login successful
   :statuscode 401: Invalid credentials
   :statuscode 429: Too many requests

Logout
------

.. http:post:: /api/auth/logout

   Invalidate the current access token.

   **Request Headers:**

   - ``Authorization: Bearer <access_token>``

   **Response:**

   .. sourcecode:: json

      {
        "message": "Successfully logged out"
      }

   :statuscode 200: Logout successful
   :statuscode 401: Invalid or expired token

Refresh Token
------------

.. http:post:: /api/auth/refresh

   Get a new access token using a refresh token.

   **Request Headers:**

   - ``Content-Type: application/json``

   **Request body:**

   .. sourcecode:: json

      {
        "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
      }

   **Response:**

   .. sourcecode:: json

      {
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "token_type": "bearer"
      }

   :statuscode 200: Token refreshed successfully
   :statuscode 401: Invalid or expired refresh token

Email Verification
-----------------

.. http:get:: /api/auth/verify/{token}

   Verify user's email address.

   **Parameters:**

   - ``token`` (string) - Verification token received via email

   **Response:**

   .. sourcecode:: json

      {
        "message": "Email verified successfully"
      }

   **Error Response:**

   .. sourcecode:: json

      {
        "detail": "Invalid or expired verification token"
      }

   :statuscode 200: Email verified successfully
   :statuscode 400: Invalid or expired token

Password Reset Request
--------------------

.. http:post:: /api/auth/password-reset

   Request a password reset link.

   **Request Headers:**

   - ``Content-Type: application/json``

   **Request body:**

   .. sourcecode:: json

      {
        "email": "user@example.com"
      }

   **Response:**

   .. sourcecode:: json

      {
        "message": "Password reset instructions sent to your email"
      }

   :statuscode 200: Reset instructions sent
   :statuscode 404: Email not found
   :statuscode 429: Too many requests

Password Reset
------------

.. http:post:: /api/auth/password-reset/{token}

   Reset password using a reset token.

   **Parameters:**

   - ``token`` (string) - Password reset token received via email

   **Request Headers:**

   - ``Content-Type: application/json``

   **Request body:**

   .. sourcecode:: json

      {
        "new_password": "newpassword123",
        "confirm_password": "newpassword123"
      }

   **Validation Rules:**

   - ``new_password``: Minimum 8 characters
   - ``confirm_password``: Must match new_password

   **Response:**

   .. sourcecode:: json

      {
        "message": "Password reset successful"
      }

   **Error Response:**

   .. sourcecode:: json

      {
        "detail": "Invalid or expired reset token"
      }

   :statuscode 200: Password reset successful
   :statuscode 400: Invalid input or token
   :statuscode 429: Too many requests 