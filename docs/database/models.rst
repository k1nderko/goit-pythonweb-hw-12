Database Models
==============

This module defines the SQLAlchemy models for the application.

User Model
---------

.. automodule:: src.database.models
   :members: User
   :undoc-members:
   :show-inheritance:

The User model represents application users with the following fields:

.. list-table::
   :header-rows: 1

   * - Field
     - Type
     - Description
   * - id
     - Integer
     - Primary key
   * - email
     - String
     - User's email address (unique)
   * - full_name
     - String
     - User's full name
   * - password
     - String
     - Hashed password
   * - role
     - Enum
     - User role (USER or ADMIN)
   * - is_verified
     - Boolean
     - Email verification status
   * - avatar_url
     - String
     - URL to user's avatar image
   * - created_at
     - DateTime
     - Creation timestamp
   * - updated_at
     - DateTime
     - Last update timestamp

Contact Model
-----------

.. automodule:: src.database.models
   :members: Contact
   :undoc-members:
   :show-inheritance:

The Contact model represents user contacts with the following fields:

.. list-table::
   :header-rows: 1

   * - Field
     - Type
     - Description
   * - id
     - Integer
     - Primary key
   * - first_name
     - String
     - Contact's first name
   * - last_name
     - String
     - Contact's last name
   * - email
     - String
     - Contact's email address
   * - phone
     - String
     - Contact's phone number
   * - birthday
     - Date
     - Contact's birthday (optional)
   * - notes
     - String
     - Additional notes (optional)
   * - owner_id
     - Integer
     - Foreign key to User model
   * - created_at
     - DateTime
     - Creation timestamp
   * - updated_at
     - DateTime
     - Last update timestamp

Relationships
-----------

The models have the following relationships:

- User has many Contacts (one-to-many)
- Contact belongs to one User (many-to-one) 