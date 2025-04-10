Authentication API
=================

Registration
-----------

.. http:post:: /api/auth/register

   Register a new user.

   **Request body:**

   .. sourcecode:: json

      {
        "email": "user@example.com",
        "password": "password123",
        "full_name": "John Doe"
      }

   **Response:**

   .. sourcecode:: json

      {
        "message": "User registered successfully. Please check your email for verification."
      }

   :statuscode 201: User registered successfully
   :statuscode 400: Invalid input data
   :statuscode 409: Email already registered

Login
-----

.. http:post:: /api/auth/login

   Login with email and password.

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
        "token_type": "bearer"
      }

   :statuscode 200: Login successful
   :statuscode 401: Invalid credentials

Email Verification
----------------

.. http:get:: /api/auth/verify/{token}

   Verify user's email address.

   **Parameters:**

   - ``token`` (string) - Verification token received via email

   **Response:**

   .. sourcecode:: json

      {
        "message": "Email verified successfully"
      }

   :statuscode 200: Email verified successfully
   :statuscode 400: Invalid or expired token 