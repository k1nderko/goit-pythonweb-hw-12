Contacts API
============

All endpoints in this section require authentication. Include the access token in the Authorization header:

.. sourcecode:: http

   Authorization: Bearer <access_token>

Create Contact
-------------

.. http:post:: /api/contacts

   Create a new contact.

   **Request Headers:**

   - ``Authorization: Bearer <access_token>``
   - ``Content-Type: application/json``

   **Request body:**

   .. sourcecode:: json

      {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "birthday": "1990-01-01",
        "additional_data": "Additional notes"
      }

   **Validation Rules:**

   - ``first_name``: Required, non-empty string
   - ``last_name``: Required, non-empty string
   - ``email``: Valid email format
   - ``phone``: Valid phone number format
   - ``birthday``: Date in YYYY-MM-DD format
   - ``additional_data``: Optional string

   **Response:**

   .. sourcecode:: json

      {
        "id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "birthday": "1990-01-01",
        "additional_data": "Additional notes",
        "created_at": "2024-03-15T10:30:00Z",
        "updated_at": "2024-03-15T10:30:00Z"
      }

   **Error Response:**

   .. sourcecode:: json

      {
        "detail": "Invalid input data"
      }

   :statuscode 201: Contact created successfully
   :statuscode 400: Invalid input data
   :statuscode 401: Unauthorized
   :statuscode 429: Too many requests

Get All Contacts
--------------

.. http:get:: /api/contacts

   Retrieve all contacts for the authenticated user.

   **Query Parameters:**

   - ``page`` (optional, default=1): Page number for pagination
   - ``per_page`` (optional, default=10): Number of items per page
   - ``sort_by`` (optional, default="created_at"): Field to sort by
   - ``order`` (optional, default="desc"): Sort order ("asc" or "desc")

   **Response:**

   .. sourcecode:: json

      {
        "items": [
          {
            "id": 1,
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone": "+1234567890",
            "birthday": "1990-01-01",
            "additional_data": "Additional notes",
            "created_at": "2024-03-15T10:30:00Z",
            "updated_at": "2024-03-15T10:30:00Z"
          }
        ],
        "total": 50,
        "page": 1,
        "per_page": 10,
        "total_pages": 5
      }

   :statuscode 200: Success
   :statuscode 401: Unauthorized
   :statuscode 429: Too many requests

Get Contact
----------

.. http:get:: /api/contacts/{contact_id}

   Retrieve a specific contact by ID.

   **Parameters:**

   - ``contact_id`` (integer) - ID of the contact to retrieve

   **Response:**

   .. sourcecode:: json

      {
        "id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "birthday": "1990-01-01",
        "additional_data": "Additional notes",
        "created_at": "2024-03-15T10:30:00Z",
        "updated_at": "2024-03-15T10:30:00Z"
      }

   **Error Response:**

   .. sourcecode:: json

      {
        "detail": "Contact not found"
      }

   :statuscode 200: Success
   :statuscode 401: Unauthorized
   :statuscode 404: Contact not found
   :statuscode 429: Too many requests

Update Contact
------------

.. http:put:: /api/contacts/{contact_id}

   Update an existing contact.

   **Parameters:**

   - ``contact_id`` (integer) - ID of the contact to update

   **Request Headers:**

   - ``Authorization: Bearer <access_token>``
   - ``Content-Type: application/json``

   **Request body:**

   .. sourcecode:: json

      {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "birthday": "1990-01-01",
        "additional_data": "Updated notes"
      }

   **Validation Rules:**

   Same as Create Contact endpoint

   **Response:**

   .. sourcecode:: json

      {
        "id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "birthday": "1990-01-01",
        "additional_data": "Updated notes",
        "created_at": "2024-03-15T10:30:00Z",
        "updated_at": "2024-03-15T11:00:00Z"
      }

   **Error Response:**

   .. sourcecode:: json

      {
        "detail": "Contact not found"
      }

   :statuscode 200: Contact updated successfully
   :statuscode 400: Invalid input data
   :statuscode 401: Unauthorized
   :statuscode 404: Contact not found
   :statuscode 429: Too many requests

Delete Contact
------------

.. http:delete:: /api/contacts/{contact_id}

   Delete a contact.

   **Parameters:**

   - ``contact_id`` (integer) - ID of the contact to delete

   **Response:**

   .. sourcecode:: json

      {
        "message": "Contact deleted successfully"
      }

   **Error Response:**

   .. sourcecode:: json

      {
        "detail": "Contact not found"
      }

   :statuscode 200: Contact deleted successfully
   :statuscode 401: Unauthorized
   :statuscode 404: Contact not found
   :statuscode 429: Too many requests

Search Contacts
-------------

.. http:get:: /api/contacts/search

   Search contacts by name or email.

   **Query Parameters:**

   - ``q`` (required): Search query string (minimum 2 characters)
   - ``page`` (optional, default=1): Page number for pagination
   - ``per_page`` (optional, default=10): Number of items per page

   **Response:**

   .. sourcecode:: json

      {
        "items": [
          {
            "id": 1,
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone": "+1234567890",
            "birthday": "1990-01-01",
            "additional_data": "Additional notes",
            "created_at": "2024-03-15T10:30:00Z",
            "updated_at": "2024-03-15T10:30:00Z"
          }
        ],
        "total": 5,
        "page": 1,
        "per_page": 10,
        "total_pages": 1
      }

   **Error Response:**

   .. sourcecode:: json

      {
        "detail": "Search query must be at least 2 characters long"
      }

   :statuscode 200: Success
   :statuscode 400: Invalid search query
   :statuscode 401: Unauthorized
   :statuscode 429: Too many requests 