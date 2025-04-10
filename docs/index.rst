.. goit-pythonweb-hw-12 documentation master file, created by
   sphinx-quickstart on Wed Apr  9 19:03:04 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

goit-pythonweb-hw-12 documentation
==================================

Add your content using ``reStructuredText`` syntax. See the
`reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html>`_
documentation for details.


Contact Management API Documentation
==================================

Welcome to the Contact Management API documentation. This API provides functionality for managing contacts with user authentication and rate limiting.

Features
--------

* User authentication with JWT tokens
* Email verification
* Contact management (CRUD operations)
* Contact search functionality
* Rate limiting
* File upload for user avatars
* Pagination for contact lists

API Structure
------------

The API is organized into several components:

.. toctree::
   :maxdepth: 2
   :caption: API Components:

   api/auth
   api/contacts
   api/schemas

Configuration
------------

Configuration settings and environment variables:

.. toctree::
   :maxdepth: 2
   :caption: Configuration:

   conf/config
   conf/mail

Database
--------

Database models and connection management:

.. toctree::
   :maxdepth: 2
   :caption: Database:

   database/models
   database/db

Repository Layer
--------------

Data access layer for contacts and users:

.. toctree::
   :maxdepth: 2
   :caption: Repository:

   repository/contacts
   repository/users

Services
--------

Business logic and external service integrations:

.. toctree::
   :maxdepth: 2
   :caption: Services:

   services/auth
   services/limiter
   services/cloudinary_service
   services/email

Getting Started
--------------

To get started with the API:

1. Clone the repository
2. Install dependencies using Poetry: ``poetry install``
3. Set up environment variables (see :doc:`conf/config`)
4. Run migrations: ``alembic upgrade head``
5. Start the server: ``uvicorn src.main:app --reload``

API Endpoints
------------

Authentication
~~~~~~~~~~~~~

* POST /api/auth/register - Register a new user
* POST /api/auth/login - Login and get access token
* GET /api/auth/verify/{token} - Verify email address
* GET /api/auth/me - Get current user info
* POST /api/auth/upload-avatar - Upload user avatar

Contacts
~~~~~~~~

* POST /api/contacts - Create a new contact
* GET /api/contacts - List all contacts
* GET /api/contacts/{id} - Get a specific contact
* PUT /api/contacts/{id} - Update a contact
* DELETE /api/contacts/{id} - Delete a contact
* GET /api/contacts/search - Search contacts

Rate Limiting
------------

The API implements rate limiting to prevent abuse:

* Authentication endpoints: 5 requests per minute
* Contact endpoints: 5 requests per minute
* Root endpoint: 5 requests per minute

In testing mode, the rate limits are increased to 1000 requests per minute.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Welcome to Contacts API documentation
===================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   api/index