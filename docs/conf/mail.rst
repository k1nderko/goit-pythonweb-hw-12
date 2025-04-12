Email Configuration
=================

The email configuration module provides settings for sending emails.

Email Settings
-------------

.. list-table::
   :header-rows: 1

   * - Setting
     - Description
     - Default
   * - MAIL_USERNAME
     - Email account username
     - test@example.com
   * - MAIL_PASSWORD
     - Email account password
     - test_password
   * - MAIL_FROM
     - Sender email address
     - test@example.com
   * - MAIL_PORT
     - SMTP server port
     - 587
   * - MAIL_SERVER
     - SMTP server address
     - smtp.gmail.com

Email Templates
-------------

The application uses the following email templates:

Verification Email
~~~~~~~~~~~~~~~~

Sent to users when they register to verify their email address.

.. sourcecode:: html

   <h1>Welcome to Contacts API!</h1>
   <p>Please verify your email address by clicking the link below:</p>
   <a href="{verification_link}">Verify Email</a>
   <p>If you did not register for this account, please ignore this email.</p>

Password Reset Email
~~~~~~~~~~~~~~~~~

Sent to users when they request a password reset.

.. sourcecode:: html

   <h1>Password Reset Request</h1>
   <p>You have requested to reset your password. Click the link below to proceed:</p>
   <a href="{reset_link}">Reset Password</a>
   <p>If you did not request a password reset, please ignore this email.</p>
   <p>This link will expire in 30 minutes.</p> 