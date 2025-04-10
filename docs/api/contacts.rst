Contacts API
===========

The contacts API provides endpoints for managing user contacts.

Create Contact
-------------

.. http:post:: /api/contacts

   Create a new contact.

   **Request body:**

   .. sourcecode:: json

      {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "birthday": "1990-01-01",
        "address": "123 Main St"
      }

   **Response:**

   .. sourcecode:: json

      {
        "id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "birthday": "1990-01-01",
        "address": "123 Main St",
        "created_at": "2024-03-20T12:00:00",
        "updated_at": "2024-03-20T12:00:00"
      }

   :statuscode 201: Contact created successfully
   :statuscode 400: Invalid input data
   :statuscode 401: Not authenticated

Get Contacts
-----------

.. http:get:: /api/contacts

   Get all contacts for the authenticated user.

   **Response:**

   .. sourcecode:: json

      [
        {
          "id": 1,
          "first_name": "John",
          "last_name": "Doe",
          "email": "john.doe@example.com",
          "phone": "+1234567890",
          "birthday": "1990-01-01",
          "address": "123 Main St",
          "created_at": "2024-03-20T12:00:00",
          "updated_at": "2024-03-20T12:00:00"
        }
      ]

   :statuscode 200: List of contacts
   :statuscode 401: Not authenticated

Get Contact
----------

.. http:get:: /api/contacts/{contact_id}

   Get a specific contact by ID.

   **Parameters:**

   - ``contact_id`` (integer) - ID of the contact

   **Response:**

   .. sourcecode:: json

      {
        "id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "birthday": "1990-01-01",
        "address": "123 Main St",
        "created_at": "2024-03-20T12:00:00",
        "updated_at": "2024-03-20T12:00:00"
      }

   :statuscode 200: Contact details
   :statuscode 401: Not authenticated
   :statuscode 404: Contact not found

Update Contact
------------

.. http:put:: /api/contacts/{contact_id}

   Update a specific contact.

   **Parameters:**

   - ``contact_id`` (integer) - ID of the contact

   **Request body:**

   .. sourcecode:: json

      {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "birthday": "1990-01-01",
        "address": "123 Main St"
      }

   **Response:**

   .. sourcecode:: json

      {
        "id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "birthday": "1990-01-01",
        "address": "123 Main St",
        "created_at": "2024-03-20T12:00:00",
        "updated_at": "2024-03-20T12:00:00"
      }

   :statuscode 200: Contact updated successfully
   :statuscode 400: Invalid input data
   :statuscode 401: Not authenticated
   :statuscode 404: Contact not found

Delete Contact
------------

.. http:delete:: /api/contacts/{contact_id}

   Delete a specific contact.

   **Parameters:**

   - ``contact_id`` (integer) - ID of the contact

   **Response:**

   .. sourcecode:: json

      {
        "message": "Contact deleted successfully"
      }

   :statuscode 200: Contact deleted successfully
   :statuscode 401: Not authenticated
   :statuscode 404: Contact not found

Search Contacts
-------------

.. http:get:: /api/contacts/search

   Search contacts by name or email.

   **Query Parameters:**

   - ``query`` (string) - Search term (minimum 1 character)

   **Response:**

   .. sourcecode:: json

      [
        {
          "id": 1,
          "first_name": "John",
          "last_name": "Doe",
          "email": "john.doe@example.com",
          "phone": "+1234567890",
          "birthday": "1990-01-01",
          "address": "123 Main St",
          "created_at": "2024-03-20T12:00:00",
          "updated_at": "2024-03-20T12:00:00"
        }
      ]

   :statuscode 200: List of matching contacts
   :statuscode 400: Invalid search query
   :statuscode 401: Not authenticated 