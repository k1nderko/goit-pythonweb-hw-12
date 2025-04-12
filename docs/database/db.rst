Database Configuration
====================

This module provides the core database configuration for the application.

Database Engine
-------------

.. automodule:: src.database.db
   :members: engine
   :undoc-members:
   :show-inheritance:

The database engine is configured with the following settings:

.. list-table::
   :header-rows: 1

   * - Setting
     - Value
     - Description
   * - DATABASE_URL
     - From environment
     - PostgreSQL connection string
   * - echo
     - True
     - Enable SQL query logging
   * - future
     - True
     - Use SQLAlchemy 2.0 style

Session Management
---------------

.. automodule:: src.database.db
   :members: SessionLocal, get_session
   :undoc-members:
   :show-inheritance:

The session management provides:

- Async session factory
- Session dependency for FastAPI
- Automatic session cleanup

Database Initialization
--------------------

.. automodule:: src.database.db
   :members: init_db
   :undoc-members:
   :show-inheritance:

The initialization function:

- Creates all database tables
- Should be called at application startup
- Uses async context manager for transaction safety

Base Model
--------

.. automodule:: src.database.db
   :members: Base
   :undoc-members:
   :show-inheritance:

The declarative base class for all models:

- Provides common functionality
- Enables SQLAlchemy ORM features
- Supports async operations 