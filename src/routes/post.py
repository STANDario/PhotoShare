from fastapi import (
    APIRouter,
    HTTPException,
    UploadFile,
    Depends,
    File,
    Form,
)
import cloudinary.uploader
import cloudinary.api
import uuid
from typing import Any
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND
from cloudinary.uploader import destroy

from src.database.models import Image
from src.schemas import PostSingle
from src.database.db import get_db
from src.repository import post
from src.conf.config import settings



class Cloudinary:
    cloudinary.config(
        cloud_name=settings.cloud_name,
        api_key=settings.api_key,
        api_secret=settings.api_secret,
        secure=True,
    )


posts_router = APIRouter(prefix="", tags=["Posts of picture"])


# публікуємо світлину
@posts_router.post("/publication", response_model=PostSingle, response_model_exclude_unset=True)
async def upload_images_user(
        file: UploadFile = File(),
        text: str = Form(...),
        db: Session = Depends(get_db),
):
    try:
        img_content = await file.read()
        public_id = f"image_{text}_{uuid.uuid4()}"

        # Завантаження на Cloudinary
        response = cloudinary.uploader.upload(
            img_content, public_id=public_id, overwrite=True, folder="publication"
        )

        # Зберігання в базі даних
        image = Image(
            url_original=response["secure_url"],
            description=text,
            updated_at=datetime.now(),
        )
        db.add(image)
        db.commit()

        # інформація про світлину
        item = await post.get_p(db=db, id=image.id)

        if not item:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND, detail="Запис не знайдений"
            )

        post_data = {
            "id": item.id,
            "url_original": item.url_original,
            "description": item.description,
            "pub_date": item.created_at,
            "img": item.url_original,
        }

        return PostSingle(**post_data)

    except HTTPException as e:
        logging.error(f"Помилка валідації форми: {e}")
        raise
    except Exception as e:
        logging.error(f"Помилка завантаження зображення: {e}")
        raise


# отримувати світлину за унікальним посиланням в БД
@posts_router.get('/{id}', response_model=PostSingle)
async def get_post(id: int, db: Session = Depends(get_db)) -> Any:
    item = await post.get_p(db=db, id=id)
    if not item:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Запис не знайдений")

    post_data = {
        "id": item.id,
        "url_original": item.url_original,
        "description": item.description,
        "pub_date": item.created_at,
        "img": item.url_original,
    }

    return PostSingle(**post_data)


# видалення світлини
@posts_router.delete('/{id}', response_model=dict, description="Видалення за id.")
async def delete_image(id: int, db: Session = Depends(get_db)) -> dict:
    item = await post.get_p(db=db, id=id)
    if not item:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Запис не знайдений")

    try:
        destroy_result = destroy(public_id=item.public_id)
        print("Cloudinary Destroy Result:", destroy_result)
    except Exception as e:
        print("Error during Cloudinary destroy:", str(e))

    db.delete(item)
    db.commit()

    return {"message": "Запис видалено успішно"}
