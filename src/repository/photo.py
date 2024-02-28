from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import status, HTTPException

from src.entity.models import Image, Tag, User
from src.services.cloudinary_service import CloudImage
from src.schemas.photo_schemas import ImageChangeResponse, ImageModel
from src.schemas.tag_schemas import TagModel, AddTagToPhoto
from src.routes.tags_routes import create_tag


async def add_image(url: str, public_id: str, description: str, db: Session, user: User) -> Image | None:
    """
    Add a new image to the database.

    Args:
        url (str): URL of the image.
        public_id (str): Public ID of the image.
        description (str): Description of the image.
        db (Session): Database session.
        user (User): Currently authenticated user.

    Returns:
        Image | None: The added image.
    """
    if not user:
        return None
    image = Image(url=url, public_id=public_id, user_id=user.id, description=description)
    db.add(image)
    db.commit()
    db.refresh(image)
    return image


async def get_photo_by_id(image_id: int, db: Session) -> Image | None:
    """
    Retrieve an image by its ID.

    Args:
        image_id (int): ID of the image.
        db (Session): Database session.

    Returns:
        Image | None: The retrieved image.
    """

    return db.query(Image).filter(Image.id == image_id).first()


async def get_photo_by_desc(description: str, db: Session):
    """
    Retrieve images by their descriptions.

    Args:
        description (str): Description to search for.
        db (Session): Database session.

    Returns:
        Any: List of images matching the description.
    """
    return db.query(Image).filter(Image.description.contains(description.lower())).all()


async def get_photo_all(skip: int, limit: int, db: Session):
    """
    Retrieve all images with pagination.

    Args:
        skip (int): Number of images to skip.
        limit (int): Maximum number of images to retrieve.
        db (Session): Database session.

    Returns:
        Any: List of images retrieved with pagination.
    """
    return db.query(Image).offset(skip).limit(limit).all()


async def update_photo(image_id: int, description: str, db: Session):
    """
    Update the description of an image.

    Args:
        image_id (int): ID of the image to update.
        description (str): New description for the image.
        db (Session): Database session.

    Returns:
        Image | None: The updated image.
    """
    image = await get_photo_by_id(image_id, db)
    if image:
        image.description = description
        db.commit()
    return image


async def delete_photo(image_id: int, db: Session):
    """
    Delete an image by its ID.

    Args:
        image_id (int): ID of the image to delete.
        db (Session): Database session.

    Returns:
        Image | None: The deleted image.
    """
    image = await get_photo_by_id(image_id, db)
    if image:
        CloudImage.delete_image(image.public_id)
        db.delete(image)
        db.commit()
    return image


async def change_size_photo(image_id: int, width: int, db: Session, user: User):
    """
    Change the size of an image.

    Args:
        image_id (int): ID of the image to resize.
        width (int): New width for the image.
        db (Session): Database session.
        user (User): Currently authenticated user.

    Returns:
        ImageChangeResponse: Response containing information about the resized image.
    """
    image = await get_photo_by_id(image_id, db)

    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

    if image.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Can`t update someones picture")

    url, public_id = CloudImage.change_size(image.public_id, width)
    new_image = Image(url=url, public_id=public_id, user_id=user.id, description=image.description)
    db.add(new_image)
    db.commit()
    db.refresh(new_image)

    image_model = ImageModel(
        id=new_image.id,
        url=new_image.url,
        description=new_image.description,
        public_id=new_image.public_id,
        user_id=user.id
    )

    return ImageChangeResponse(image=image_model, detail="Image has been resized and added")


async def fade_edge_photo(image_id, db: Session, user: User):
    """
    Apply a fade effect to an image.

    Args:
        image_id: ID of the image to apply the fade effect.
        db (Session): Database session.
        user (User): Currently authenticated user.

    Returns:
        ImageChangeResponse: Response containing information about the image with the fade effect.
    """
    image = await get_photo_by_id(image_id, db)

    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

    if image.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Can`t update someones picture")

    url, public_id = CloudImage.fade_edge(image.public_id)
    new_image = Image(url=url, public_id=public_id, user_id=user.id, description=image.description)
    db.add(new_image)
    db.commit()
    db.refresh(new_image)

    image_model = ImageModel(
        id=new_image.id,
        url=new_image.url,
        description=new_image.description,
        public_id=new_image.public_id,
        user_id=user.id
    )

    return ImageChangeResponse(image=image_model, detail="Image with fade effect has been added")


async def black_white_photo(image_id, db: Session, user: User):
    """
    Convert an image to black and white.

    Args:
        image_id: ID of the image to convert.
        db (Session): Database session.
        user (User): Currently authenticated user.

    Returns:
        ImageChangeResponse: Response containing information about the converted image.
    """
    image = await get_photo_by_id(image_id, db)

    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

    if image.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Can`t update someones picture")

    url, public_id = CloudImage.black_white(image.public_id)
    new_image = Image(url=url, public_id=public_id, user_id=user.id, description=image.description)
    db.add(new_image)
    db.commit()
    db.refresh(new_image)

    image_model = ImageModel(
        id=new_image.id,
        url=new_image.url,
        description=new_image.description,
        public_id=new_image.public_id,
        user_id=user.id
    )

    return ImageChangeResponse(image=image_model, detail="Image with fade effect has been added")


async def add_tag(image_id: int, tag_name: str, db: Session, user: User):
    """
    Add a tag to an image.

    Args:
        image_id (int): ID of the image to add the tag to.
        tag_name (str): Name of the tag to add.
        db (Session): Database session.
        user (User): Currently authenticated user.

    Returns:
        AddTagToPhoto: Response containing the added tag name.
    """
    image = await get_photo_by_id(image_id, db)

    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

    if image.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Can`t update someones picture")

    if len(image.tags) >= 5:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Only five tags allowed")

    tag = db.execute(select(Tag).filter(Tag.tag_name == tag_name.lower()))
    tag = tag.scalar()

    if tag is None:
        tag_model = TagModel(tag_name=tag_name)
        tag = await create_tag(tag_model, db)

    image.tags.append(tag)

    db.commit()
    db.refresh(image)

    return AddTagToPhoto(tag=tag.tag_name)
