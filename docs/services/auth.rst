Authentication Service
===================

This module provides authentication and authorization functionality.

Auth Service
----------

.. automodule:: src.services.auth
   :members: AuthService
   :undoc-members:
   :show-inheritance:

The AuthService class provides the following operations:

Create Access Token
----------------

.. automodule:: src.services.auth
   :members: AuthService.create_access_token
   :undoc-members:
   :show-inheritance:

Creates a JWT access token.

Create Refresh Token
-----------------

.. automodule:: src.services.auth
   :members: AuthService.create_refresh_token
   :undoc-members:
   :show-inheritance:

Creates a JWT refresh token.

Verify Password
------------

.. automodule:: src.services.auth
   :members: AuthService.verify_password
   :undoc-members:
   :show-inheritance:

Verifies a password against a hash.

Get Password Hash
--------------

.. automodule:: src.services.auth
   :members: AuthService.get_password_hash
   :undoc-members:
   :show-inheritance:

Hashes a password.

Create User
---------

.. automodule:: src.services.auth
   :members: AuthService.create_user
   :undoc-members:
   :show-inheritance:

Creates a new user.

Authenticate User
--------------

.. automodule:: src.services.auth
   :members: AuthService.authenticate_user
   :undoc-members:
   :show-inheritance:

Authenticates a user with email and password.

Parameters
---------

.. list-table::
   :header-rows: 1

   * - Parameter
     - Type
     - Description
   * - data
     - dict
     - Token data (email, role)
   * - expires_delta
     - timedelta
     - Token expiration time
   * - plain_password
     - str
     - Plain text password
   * - hashed_password
     - str
     - Hashed password
   * - user_data
     - dict
     - User data for creation
   * - email
     - str
     - User's email
   * - password
     - str
     - User's password

Return Values
-----------

.. list-table::
   :header-rows: 1

   * - Method
     - Return Type
     - Description
   * - create_access_token
     - str
     - JWT access token
   * - create_refresh_token
     - str
     - JWT refresh token
   * - verify_password
     - bool
     - True if password matches
   * - get_password_hash
     - str
     - Hashed password
   * - create_user
     - User
     - Created user
   * - authenticate_user
     - User
     - Authenticated user 