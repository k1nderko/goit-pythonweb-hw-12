Cloudinary Service
===============

This module provides image upload and management functionality using Cloudinary.

Cloudinary Service
---------------

.. automodule:: src.services.cloudinary_service
   :members: CloudinaryService
   :undoc-members:
   :show-inheritance:

The CloudinaryService class provides the following operations:

Upload Image
---------

.. automodule:: src.services.cloudinary_service
   :members: CloudinaryService.upload_image
   :undoc-members:
   :show-inheritance:

Uploads an image to Cloudinary.

Delete Image
---------

.. automodule:: src.services.cloudinary_service
   :members: CloudinaryService.delete_image
   :undoc-members:
   :show-inheritance:

Deletes an image from Cloudinary.

Configuration
-----------

The Cloudinary service is configured with the following settings:

.. list-table::
   :header-rows: 1

   * - Setting
     - Value
     - Description
   * - CLOUDINARY_NAME
     - From environment
     - Cloudinary cloud name
   * - CLOUDINARY_API_KEY
     - From environment
     - Cloudinary API key
   * - CLOUDINARY_API_SECRET
     - From environment
     - Cloudinary API secret

Image Settings
-----------

The following image settings are applied:

.. list-table::
   :header-rows: 1

   * - Setting
     - Value
     - Description
   * - folder
     - "avatars"
     - Storage folder
   * - width
     - 250
     - Image width
   * - height
     - 250
     - Image height
   * - crop
     - "fill"
     - Crop mode
   * - quality
     - "auto"
     - Image quality

Parameters
---------

.. list-table::
   :header-rows: 1

   * - Parameter
     - Type
     - Description
   * - file
     - UploadFile
     - Image file to upload
   * - public_id
     - str
     - Public ID of image to delete

Return Values
-----------

.. list-table::
   :header-rows: 1

   * - Method
     - Return Type
     - Description
   * - upload_image
     - str
     - URL of uploaded image
   * - delete_image
     - None
     - No return value 