from typing import List

from fastapi import APIRouter, Depends, status, UploadFile, File, HTTPException, Query
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.entity.models import User, Role
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
from src.services.auth_service import get_current_user
from src.services.role_service import all_roles


router = APIRouter(prefix="/images", tags=["images"])


@router.post("/upload", response_model=ImageModel, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(all_roles)])
async def upload_photo(description: str = None, file: UploadFile = File(), db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user)):
    """
    Uploads a photo.

    Args:
        description (str, optional): Description of the photo. Defaults to None.
        file (UploadFile, optional): The file uploaded. Defaults to File(...).
        db (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (User, optional): Current user. Defaults to Depends(get_current_user).

    Raises:
        HTTPException: If the image cannot be uploaded.

    Returns:
        ImageModel: The uploaded image data.
    """
    public_id = CloudImage.generate_name_image(current_user.email)
    upload_file = CloudImage.upload_image(file.file, public_id)
    src_url = CloudImage.get_url_for_image(public_id, upload_file)
    image = await repository_photo.add_image(src_url, public_id, description, db, current_user)

    return image


# Пошук за входженням опису в світлину
@router.get("/search", response_model=List[ImageAllResponse], dependencies=[Depends(all_roles)])
async def get_photo_by_description(description: str, db: Session = Depends(get_db),
                                   current_user: User = Depends(get_current_user)):
    """
    Get images that match the given description.

    Args:
        description (str): The description to search for.
        db (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (User, optional): Current user. Defaults to Depends(get_current_user).

    Raises:
        HTTPException: If an internal server error occurs or no images are found.

    Returns:
        List[ImageAllResponse]: List of images matching the description.
    """
    try:
        image = await repository_photo.get_photo_by_desc(description, db)
        if not image:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

        return image

    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# Повертаємо усі світлини
@router.get("/get_all", response_model=List[ImageAllResponse], dependencies=[Depends(all_roles)])
async def get_all_photo(skip: int = 0, limit: int = Query(default=10, le=100, ge=10),
                        db: Session = Depends(get_db),
                        current_user: User = Depends(get_current_user)):
    """
    Get all images.

    Args:
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 10.
        db (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (User, optional): Current user. Defaults to Depends(get_current_user).

    Raises:
        HTTPException: If an internal server error occurs or no images are found.

    Returns:
        List[ImageAllResponse]: List of all images.
    """
    try:
        image = await repository_photo.get_photo_all(skip, limit, db)
        if not image:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

        return image

    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# Пошук світлини за id
@router.get("/{image_id}", response_model=ImageURLResponse, dependencies=[Depends(all_roles)])
async def get_photo_url(image_id: int, db: Session = Depends(get_db),
                        current_user: User = Depends(get_current_user)):
    """
    Get image by ID.

    Args:
        image_id (int): The ID of the image to retrieve.
        db (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (User, optional): Current user. Defaults to Depends(get_current_user).

    Raises:
        HTTPException: If an internal server error occurs or the image is not found.

    Returns:
        ImageURLResponse: Details of the retrieved image.
    """
    try:
        image = await repository_photo.get_photo_by_id(image_id, db)
        if not image:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

        return image

    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/{image_id}/update", response_model=ImageUpdateResponse, dependencies=[Depends(all_roles)])
async def update_photo(image_id: int, description: str, db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user)):
    """
    Update image description.

    Args:
        image_id (int): The ID of the image to update.
        description (str): The new description for the image.
        db (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (User, optional): Current user. Defaults to Depends(get_current_user).

    Raises:
        HTTPException: If an internal server error occurs, the image is not found,
            or the user is not authorized to update the image.

    Returns:
        ImageUpdateResponse: Details of the updated image.
    """
    try:
        image = await repository_photo.get_photo_by_id(image_id, db)
        if not image:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

        if image.user_id != current_user.id and current_user.role != Role.admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Can`t update someones picture")

        updated_image = await repository_photo.update_photo(image_id, description, db)
        return updated_image

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{image_id}", response_model=ImageDeleteModel, dependencies=[Depends(all_roles)])
async def delete_model(image_id, db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user)):
    """
    Delete image by ID.

    Args:
        image_id (int): The ID of the image to delete.
        db (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (User, optional): Current user. Defaults to Depends(get_current_user).

    Raises:
        HTTPException: If an internal server error occurs, the image is not found,
            or the user is not authorized to delete the image.

    Returns:
        ImageDeleteModel: Details of the deleted image.
    """
    try:
        image = await repository_photo.get_photo_by_id(image_id, db)
        if not image:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

        if image.user_id != current_user.id and current_user.role != Role.admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Can`t delete someones picture")

        deleted_image = await repository_photo.delete_photo(image_id, db)
        return deleted_image

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# Міняємо розмір зображення, погрішує якість при зміні
@router.post("/change_size", response_model=ImageChangeResponse, status_code=status.HTTP_201_CREATED)
async def change_size(image_id: int, width: int, db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_user)):
    """
    Change the size of an image.

    Args:
        image_id (int): The ID of the image to resize.
        width (int): The new width of the image.
        db (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (User, optional): Current user. Defaults to Depends(get_current_user).

    Returns:
        ImageChangeResponse: Details of the resized image.
    """
    image = await repository_photo.change_size_photo(image_id, width, db, current_user)

    return image


# Додаємо вицвілі кути на зображення
@router.post("/fade_edges", response_model=ImageChangeResponse, status_code=status.HTTP_201_CREATED)
async def fade_edges_image(image_id, db: Session = Depends(get_db),
                           current_user: User = Depends(get_current_user)):
    """
    Add faded edges to an image.

    Args:
        image_id: The ID of the image to edit.
        db (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (User, optional): Current user. Defaults to Depends(get_current_user).

    Returns:
        ImageChangeResponse: Details of the edited image.
    """
    image = await repository_photo.fade_edge_photo(image_id, db, current_user)

    return image


# Робить фото чорно-білим
@router.post("/black_white", response_model=ImageChangeResponse, status_code=status.HTTP_201_CREATED)
async def black_white_image(image_id, db: Session = Depends(get_db),
                            current_user: User = Depends(get_current_user)):
    """
    Convert an image to black and white.

    Args:
        image_id: The ID of the image to convert.
        db (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (User, optional): Current user. Defaults to Depends(get_current_user).

    Returns:
        ImageChangeResponse: Details of the converted image.
    """
    image = await repository_photo.black_white_photo(image_id, db, current_user)

    return image


@router.post("/add_tag", response_model=AddTag, dependencies=[Depends(all_roles)])
async def add_tag(image_id: int, tag: str, db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    """
    Add a tag to an image.

    Args:
        image_id (int): The ID of the image to tag.
        tag (str): The tag to add.
        db (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (User, optional): Current user. Defaults to Depends(get_current_user).

    Raises:
        HTTPException: If an internal server error occurs or the user is not authorized to add a tag.

    Returns:
        AddTag: Details of the tagged image.
    """
    try:
        image = await repository_photo.add_tag(image_id, tag, db, current_user)

        if image.user_id != current_user.id and current_user.role != Role.admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Can`t delete someones picture")

        return image

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
