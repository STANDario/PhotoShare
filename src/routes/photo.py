from fastapi import APIRouter, Depends, status, UploadFile, File, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.schemas import ImageModel, ImageURLResponse, ImageUpdateResponse, ImageDeleteModel
from src.database.db import get_db
from src.services.cloudinary_service import CloudImage
from src.repository import photo as repository_photo


router = APIRouter(prefix="/images", tags=["images"])


@router.post("/upload", response_model=ImageModel, status_code=status.HTTP_201_CREATED)
async def upload_photo(description: str = None, file: UploadFile = File(), db: Session = Depends(get_db)):
    public_id = CloudImage.generate_name_image()
    upload_file = CloudImage.upload_image(file.file, public_id)
    src_url = CloudImage.get_url_for_image(public_id, upload_file)
    image = await repository_photo.add_image(src_url, public_id, description, db)

    return image


@router.get("/{image_id}]", response_model=ImageURLResponse)
async def get_photo_url(image_id: int, db: Session = Depends(get_db)):
    try:
        image = await repository_photo.get_photo_by_id(image_id, db)
        if not image:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

        return image

    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.patch("/{image_id}/update", response_model=ImageUpdateResponse)
async def update_photo(image_id: int, description: str, db: Session = Depends(get_db)):
    try:
        image = await repository_photo.get_photo_by_id(image_id, db)
        if not image:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

        updated_image = await repository_photo.update_photo(image_id, description, db)
        return updated_image

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{image_id}", response_model=ImageDeleteModel)
async def delete_model(image_id, db: Session = Depends(get_db)):
    try:
        image = await repository_photo.get_photo_by_id(image_id, db)
        if not image:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

        deleted_image = await repository_photo.delete_photo(image_id, db)
        return deleted_image

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
