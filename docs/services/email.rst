Email Service
===========

This module provides email sending functionality.

Email Service
-----------

.. automodule:: src.services.email
   :members: EmailService
   :undoc-members:
   :show-inheritance:

The EmailService class provides the following operations:

Send Email
--------

.. automodule:: src.services.email
   :members: EmailService.send_email
   :undoc-members:
   :show-inheritance:

Sends an email.

Send Verification Email
--------------------

.. automodule:: src.services.email
   :members: EmailService.send_verification_email
   :undoc-members:
   :show-inheritance:

Sends a verification email to a user.

Send Password Reset Email
----------------------

.. automodule:: src.services.email
   :members: EmailService.send_password_reset_email
   :undoc-members:
   :show-inheritance:

Sends a password reset email to a user.

Configuration
-----------

The email service is configured with the following settings:

.. list-table::
   :header-rows: 1

   * - Setting
     - Value
     - Description
   * - MAIL_USERNAME
     - From environment
     - Email account username
   * - MAIL_PASSWORD
     - From environment
     - Email account password
   * - MAIL_FROM
     - From environment
     - Sender email address
   * - MAIL_PORT
     - From environment
     - SMTP server port
   * - MAIL_SERVER
     - From environment
     - SMTP server address

Email Templates
------------

The following email templates are used:

Verification Email
~~~~~~~~~~~~~~~

.. sourcecode:: html

   <h1>Welcome to Contacts API!</h1>
   <p>Please verify your email address by clicking the link below:</p>
   <a href="{verification_link}">Verify Email</a>
   <p>If you did not register for this account, please ignore this email.</p>

Password Reset Email
~~~~~~~~~~~~~~~~~

.. sourcecode:: html

   <h1>Password Reset Request</h1>
   <p>You have requested to reset your password. Click the link below to proceed:</p>
   <a href="{reset_link}">Reset Password</a>
   <p>If you did not request a password reset, please ignore this email.</p>
   <p>This link will expire in 30 minutes.</p>

Parameters
---------

.. list-table::
   :header-rows: 1

   * - Parameter
     - Type
     - Description
   * - email_to
     - str
     - Recipient email address
   * - subject
     - str
     - Email subject
   * - body
     - str
     - Email body (HTML)
   * - verification_link
     - str
     - Email verification link
   * - reset_link
     - str
     - Password reset link

Return Values
-----------

.. list-table::
   :header-rows: 1

   * - Method
     - Return Type
     - Description
   * - send_email
     - None
     - No return value
   * - send_verification_email
     - None
     - No return value
   * - send_password_reset_email
     - None
     - No return value 