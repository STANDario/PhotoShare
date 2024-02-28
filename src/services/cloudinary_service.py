import hashlib
from datetime import datetime
from typing import Tuple

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
    def generate_name_image(email: str) -> str:
        name = hashlib.sha256(email.encode("utf-8")).hexdigest()[:12]
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

    @staticmethod
    def change_size(public_id: str, width: int) -> Tuple[str, str]:
        image = cloudinary.CloudinaryImage(public_id).image(
            transformation=[{"width": width, "crop": "pad"}]
        )
        url = image.split('"')
        upload_image = cloudinary.uploader.upload(url[1], folder="photo_share")
        return upload_image["url"], upload_image["public_id"]

    @staticmethod
    def fade_edge(public_id: str, effect: str = "vignette") -> Tuple[str, str]:
        image = cloudinary.CloudinaryImage(public_id).image(effect=effect)
        url = image.split('"')
        upload_image = cloudinary.uploader.upload(url[1], folder="photo_share")
        return upload_image["url"], upload_image["public_id"]

    @staticmethod
    def black_white(public_id: str, effect: str = "art:audrey") -> Tuple[str, str]:
        image = cloudinary.CloudinaryImage(public_id).image(effect=effect)
        url = image.split('"')
        upload_image = cloudinary.uploader.upload(url[1], folder="photo_share")
        return upload_image["url"], upload_image["public_id"]
