import hashlib
from datetime import datetime

import cloudinary
import cloudinary.uploader

from src.conf.config import settings


class CloudImage:
    cloudinary.config(
        cloud_name=settings.cloud_name,
        api_key=settings.api_key,
        api_secret=settings.api_secret,
        secure=True,
    )

    @staticmethod
    def generate_name_image() -> str:
        name = hashlib.sha256("email".encode("utf-8")).hexdigest()[:12]
        time = datetime.now()
        return f"photo_share/{name}{time}"

    @staticmethod
    def upload_image(file, public_id: str) -> dict:
        upload_file = cloudinary.uploader.upload(file, public_id=public_id)
        return upload_file

    @staticmethod
    def get_url_for_image(public_id, upload_file) -> str:
        src_url = cloudinary.CloudinaryImage(public_id).build_url(
            version=upload_file.get("version")
        )
        return src_url

    @staticmethod
    def delete_image(public_id: str):
        cloudinary.uploader.destroy(public_id, resource_type="image")
        return f"{public_id} deleted"
