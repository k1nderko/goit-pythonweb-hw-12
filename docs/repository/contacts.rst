Contacts Repository
=================

This module provides data access operations for contacts.

Contact Repository
---------------

.. automodule:: src.repository.contacts
   :members: ContactRepository
   :undoc-members:
   :show-inheritance:

The ContactRepository class provides the following operations:

Create Contact
------------

.. automodule:: src.repository.contacts
   :members: ContactRepository.create_contact
   :undoc-members:
   :show-inheritance:

Creates a new contact for a user.

Get Contact
---------

.. automodule:: src.repository.contacts
   :members: ContactRepository.get_contact
   :undoc-members:
   :show-inheritance:

Retrieves a specific contact by ID.

Get User Contacts
--------------

.. automodule:: src.repository.contacts
   :members: ContactRepository.get_user_contacts
   :undoc-members:
   :show-inheritance:

Retrieves all contacts for a user.

Update Contact
-----------

.. automodule:: src.repository.contacts
   :members: ContactRepository.update_contact
   :undoc-members:
   :show-inheritance:

Updates an existing contact.

Delete Contact
-----------

.. automodule:: src.repository.contacts
   :members: ContactRepository.delete_contact
   :undoc-members:
   :show-inheritance:

Deletes a contact.

Search Contacts
------------

.. automodule:: src.repository.contacts
   :members: ContactRepository.search_contacts
   :undoc-members:
   :show-inheritance:

Searches contacts by name or email.

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
     - ID of the user who owns the contacts
   * - contact_id
     - int
     - ID of the contact to retrieve/update/delete
   * - contact_data
     - dict
     - Contact data for creation/update
   * - query
     - str
     - Search query for name or email
   * - skip
     - int
     - Number of records to skip (pagination)
   * - limit
     - int
     - Maximum number of records to return (pagination)

Return Values
-----------

.. list-table::
   :header-rows: 1

   * - Method
     - Return Type
     - Description
   * - create_contact
     - Contact
     - Created contact
   * - get_contact
     - Contact
     - Retrieved contact
   * - get_user_contacts
     - List[Contact]
     - List of user's contacts
   * - update_contact
     - Contact
     - Updated contact
   * - delete_contact
     - None
     - No return value
   * - search_contacts
     - List[Contact]
     - List of matching contacts 