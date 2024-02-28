from typing import List

from fastapi import APIRouter, Depends, status, UploadFile, File, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.schemas.photo_schemas import (
    ImageModel,
    ImageURLResponse,
    ImageUpdateResponse,
    ImageDeleteModel,
    ImageAllResponse,
    ImageChangeResponse
)
from src.schemas.tag_schemas import AddTag
from src.database.db import get_db
from src.services.cloudinary_service import CloudImage
from src.repository import photo as repository_photo

router = APIRouter(prefix="/images", tags=["images"])


@router.post("/upload", response_model=ImageModel, status_code=status.HTTP_201_CREATED)
async def upload_photo(description: str = None, file: UploadFile = File(), db: Session = Depends(get_db)):
    """
    Uploads a photo.

    This endpoint allows users to upload a photo with an optional description.

    :param description: The description of the photo.
    :type description: str
    :param file: The photo file to upload.
    :type file: UploadFile
    :param db: Database session.
    :type db: Session
    :return: The uploaded photo.
    :rtype: ImageModel
    """
    public_id = CloudImage.generate_name_image()
    upload_file = CloudImage.upload_image(file.file, public_id)
    src_url = CloudImage.get_url_for_image(public_id, upload_file)
    image = await repository_photo.add_image(src_url, public_id, description, db)

    return image


# Пошук за входженням опису в світлину
@router.get("/search", response_model=List[ImageAllResponse])
async def get_photo_by_description(description: str, db: Session = Depends(get_db)):
    """
    Retrieves photos by their description.

    This endpoint retrieves all photos whose description contains the specified text.

    :param description: The text to search for in photo descriptions.
    :type description: str
    :param db: Database session.
    :type db: Session
    :return: A list of matching photos.
    :rtype: List[ImageAllResponse]
    """
    try:
        image = await repository_photo.get_photo_by_desc(description, db)
        if not image:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

        return image

    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# Повертаємо усі світлини
@router.get("/get_all", response_model=List[ImageAllResponse])
async def get_all_photo(db: Session = Depends(get_db)):
    """
    Retrieves all photos.

    This endpoint retrieves all photos stored in the database.

    :param db: Database session.
    :type db: Session
    :return: A list of all photos.
    :rtype: List[ImageAllResponse]
    """
    try:
        image = await repository_photo.get_photo_all(db)
        if not image:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

        return image

    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# Пошук світлини за id
@router.get("/{image_id}", response_model=ImageURLResponse)
async def get_photo_url(image_id: int, db: Session = Depends(get_db)):
    """
    Retrieves a photo by its ID.

    This endpoint retrieves a photo by its unique identifier.

    :param image_id: The ID of the photo to retrieve.
    :type image_id: int
    :param db: Database session.
    :type db: Session
    :return: The requested photo.
    :rtype: ImageURLResponse
    """
    try:
        image = await repository_photo.get_photo_by_id(image_id, db)
        if not image:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

        return image

    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/{image_id}/update", response_model=ImageUpdateResponse)
async def update_photo(image_id: int, description: str, db: Session = Depends(get_db)):
    """
    Updates a photo's description.

    This endpoint updates the description of a photo with the specified ID.

    :param image_id: The ID of the photo to update.
    :type image_id: int
    :param description: The new description for the photo.
    :type description: str
    :param db: Database session.
    :type db: Session
    :return: The updated photo.
    :rtype: ImageUpdateResponse
    """
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
    """
    Deletes a photo.

    This endpoint deletes a photo with the specified ID.

    :param image_id: The ID of the photo to delete.
    :type image_id: int
    :param db: Database session.
    :type db: Session
    :return: The deleted photo.
    :rtype: ImageDeleteModel
    """
    try:
        image = await repository_photo.get_photo_by_id(image_id, db)
        if not image:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

        deleted_image = await repository_photo.delete_photo(image_id, db)
        return deleted_image

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# Міняємо розмір зображення, погрішує якість при зміні
@router.post("/change_size", response_model=ImageChangeResponse, status_code=status.HTTP_201_CREATED)
async def change_size(image_id: int, width: int, db: Session = Depends(get_db)):
    """
    Change the size of the image.

    This endpoint resizes the image with the specified ID to the given width.

    :param image_id: The ID of the image to resize.
    :type image_id: int
    :param width: The new width of the image.
    :type width: int
    :param db: Database session.
    :type db: Session
    :return: Response with the changed image.
    :rtype: ImageChangeResponse
    """
    image = await repository_photo.change_size_photo(image_id, width, db)

    return image


# Додаємо вицвілі кути на зображення
@router.post("/fade_edges", response_model=ImageChangeResponse, status_code=status.HTTP_201_CREATED)
async def fade_edges_image(image_id, db: Session = Depends(get_db)):
    """
    Add faded edges to the image.

    This endpoint adds faded edges to the image with the specified ID.

    :param image_id: The ID of the image.
    :type image_id: int
    :param db: Database session.
    :type db: Session
    :return: Response with the image containing faded edges.
    :rtype: ImageChangeResponse
    """
    image = await repository_photo.fade_edge_photo(image_id, db)

    return image


# Робить фото чорно-білим
@router.post("/black_white", response_model=ImageChangeResponse, status_code=status.HTTP_201_CREATED)
async def black_white_image(image_id, db: Session = Depends(get_db)):
    """
    Convert the image to black and white.

    This endpoint converts the image with the specified ID to black and white.

    :param image_id: The ID of the image.
    :type image_id: int
    :param db: Database session.
    :type db: Session
    :return: Response with the black and white image.
    :rtype: ImageChangeResponse
    """
    image = await repository_photo.black_white_photo(image_id, db)

    return image


@router.post("/add_tag", response_model=AddTag)
async def add_tag(image_id: int, tag: str, db: Session = Depends(get_db)):
    """
    Add a tag to the image.

    This endpoint adds a tag to the image with the specified ID.

    :param image_id: The ID of the image.
    :type image_id: int
    :param tag: The tag to add to the image.
    :type tag: str
    :param db: Database session.
    :type db: Session
    :return: Response indicating the tag added to the image.
    :rtype: AddTag
    """
    try:
        image = await repository_photo.add_tag(image_id, tag, db)
        return image

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
