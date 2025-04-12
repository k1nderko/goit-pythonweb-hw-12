Users Repository
==============

This module provides data access operations for users.

User Repository
-------------

.. automodule:: src.repository.users
   :members: UserRepository
   :undoc-members:
   :show-inheritance:

The UserRepository class provides the following operations:

Create User
---------

.. automodule:: src.repository.users
   :members: UserRepository.create_user
   :undoc-members:
   :show-inheritance:

Creates a new user.

Get User
-------

.. automodule:: src.repository.users
   :members: UserRepository.get_user
   :undoc-members:
   :show-inheritance:

Retrieves a user by ID.

Get User by Email
--------------

.. automodule:: src.repository.users
   :members: UserRepository.get_user_by_email
   :undoc-members:
   :show-inheritance:

Retrieves a user by email address.

Update User
---------

.. automodule:: src.repository.users
   :members: UserRepository.update_user
   :undoc-members:
   :show-inheritance:

Updates an existing user.

Verify User
---------

.. automodule:: src.repository.users
   :members: UserRepository.verify_user
   :undoc-members:
   :show-inheritance:

Marks a user's email as verified.

Update Avatar
-----------

.. automodule:: src.repository.users
   :members: UserRepository.update_avatar
   :undoc-members:
   :show-inheritance:

Updates a user's avatar URL.

Parameters
---------

.. list-table::
   :header-rows: 1

   * - Parameter
     - Type
     - Description
   * - db
     - AsyncSession
     - Database session
   * - user_id
     - int
     - ID of the user
   * - email
     - str
     - User's email address
   * - user_data
     - dict
     - User data for creation/update
   * - avatar_url
     - str
     - URL of the user's avatar

Return Values
-----------

.. list-table::
   :header-rows: 1

   * - Method
     - Return Type
     - Description
   * - create_user
     - User
     - Created user
   * - get_user
     - User
     - Retrieved user
   * - get_user_by_email
     - User
     - Retrieved user
   * - update_user
     - User
     - Updated user
   * - verify_user
     - User
     - Verified user
   * - update_avatar
     - User
     - User with updated avatar 