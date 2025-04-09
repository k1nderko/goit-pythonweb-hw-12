import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

def upload_avatar(file, public_id):
    """
        Upload an avatar image to Cloudinary, resize it, and return the secure URL.

        Args:
            file: The image file to upload. Can be a file-like object or a file path.
            public_id (str): The public ID to assign to the uploaded file.

        Returns:
            str: The secure URL of the uploaded avatar image.
        """
    result = cloudinary.uploader.upload(
        file,
        public_id=public_id,
        folder="avatars",
        overwrite=True,
        transformation=[
            {"width": 250, "height": 250, "crop": "fill", "gravity": "face"}
        ]
    )
    return result.get("secure_url")
