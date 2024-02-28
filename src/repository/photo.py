from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import status, HTTPException

from src.entity.models import Image, Tag
from src.services.cloudinary_service import CloudImage
from src.schemas.photo_schemas import ImageChangeResponse, ImageModel
from src.schemas.tag_schemas import TagModel, AddTagToPhoto
from src.routes.tags_routes import create_tag


async def add_image(url: str, public_id: str, description: str, db: Session) -> Image | None:
    """
    Add an image to the database.

    This function adds an image with the provided URL, public ID, and description to the database.

    :param url: URL of the image.
    :type url: str
    :param public_id: Public ID of the image.
    :type public_id: str
    :param description: Description of the image.
    :type description: str
    :param db: Database session.
    :type db: Session
    :return: The added image.
    :rtype: Image | None
    """
    image = Image(url=url, public_id=public_id, description=description)
    db.add(image)
    db.commit()
    db.refresh(image)
    return image


async def get_photo_by_id(image_id: int, db: Session) -> Image | None:
    """
    Get an image by its ID.

    This function retrieves an image by its ID from the database.

    :param image_id: The ID of the image.
    :type image_id: int
    :param db: Database session.
    :type db: Session
    :return: The image with the specified ID.
    :rtype: Image | None
    """
    return db.query(Image).filter(Image.id == image_id).first()


async def get_photo_by_desc(description: str, db: Session):
    """
    Get images by description.

    This function retrieves images that contain the provided description.

    :param description: The description to search for.
    :type description: str
    :param db: Database session.
    :type db: Session
    """
    return db.query(Image).filter(Image.description.contains(description.lower())).all()


async def get_photo_all(db):
    """
    Get all images.

    This function retrieves all images from the database.

    :param db: Database session.
    :type db: Session
    """
    return db.query(Image).filter().all()


async def update_photo(image_id: int, description: str, db: Session):
    """
    Update an image's description.

    This function updates the description of the image with the specified ID.

    :param image_id: The ID of the image to update.
    :type image_id: int
    :param description: The new description for the image.
    :type description: str
    :param db: Database session.
    :type db: Session
    :return: The updated image.
    :rtype: Image | None
    """
    image = await get_photo_by_id(image_id, db)
    if image:
        image.description = description
        db.commit()
    return image


async def delete_photo(image_id: int, db: Session):
    """
    Delete an image.

    This function deletes the image with the specified ID.

    :param image_id: The ID of the image to delete.
    :type image_id: int
    :param db: Database session.
    :type db: Session
    :return: The deleted image.
    :rtype: Image | None
    """
    image = await get_photo_by_id(image_id, db)
    if image:
        CloudImage.delete_image(image.public_id)
        db.delete(image)
        db.commit()
    return image


async def change_size_photo(image_id: int, width: int, db: Session):
    """
    Change the size of an image.

    This function resizes the image with the specified ID to the given width.

    :param image_id: The ID of the image to resize.
    :type image_id: int
    :param width: The new width for the image.
    :type width: int
    :param db: Database session.
    :type db: Session
    :return: The resized image.
    :rtype: ImageChangeResponse
    """
    image = await get_photo_by_id(image_id, db)

    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

    url, public_id = CloudImage.change_size(image.public_id, width)
    new_image = Image(url=url, public_id=public_id, description=image.description)
    db.add(new_image)
    db.commit()
    db.refresh(new_image)

    image_model = ImageModel(
        id=new_image.id,
        url=new_image.url,
        description=new_image.description,
        public_id=new_image.public_id
    )

    return ImageChangeResponse(image=image_model, detail="Image has been resized and added")


async def fade_edge_photo(image_id, db: Session):
    """
    Add fade effect to an image.

    This function adds a fade effect to the image with the specified ID.

    :param image_id: The ID of the image to add the fade effect to.
    :type image_id: int
    :param db: Database session.
    :type db: Session
    :return: Response containing the modified image information.
    :rtype: ImageChangeResponse
    """
    image = await get_photo_by_id(image_id, db)

    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

    url, public_id = CloudImage.fade_edge(image.public_id)
    new_image = Image(url=url, public_id=public_id, description=image.description)
    db.add(new_image)
    db.commit()
    db.refresh(new_image)

    image_model = ImageModel(
        id=new_image.id,
        url=new_image.url,
        description=new_image.description,
        public_id=new_image.public_id
    )

    return ImageChangeResponse(image=image_model, detail="Image with fade effect has been added")


async def black_white_photo(image_id, db: Session):
    """
    Convert an image to black and white.

    This function converts the image with the specified ID to black and white.

    :param image_id: The ID of the image to convert.
    :type image_id: int
    :param db: Database session.
    :type db: Session
    :return: Response containing the modified image information.
    :rtype: ImageChangeResponse
    """
    image = await get_photo_by_id(image_id, db)

    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

    url, public_id = CloudImage.black_white(image.public_id)
    new_image = Image(url=url, public_id=public_id, description=image.description)
    db.add(new_image)
    db.commit()
    db.refresh(new_image)

    image_model = ImageModel(
        id=new_image.id,
        url=new_image.url,
        description=new_image.description,
        public_id=new_image.public_id
    )

    return ImageChangeResponse(image=image_model, detail="Image with fade effect has been added")


async def add_tag(image_id: int, tag_name: str, db: Session):
    """
    Add a tag to an image.

    This function adds a tag with the specified name to the image with the given ID.

    :param image_id: The ID of the image to add the tag to.
    :type image_id: int
    :param tag_name: The name of the tag to add.
    :type tag_name: str
    :param db: Database session.
    :type db: Session
    :return: Response containing the added tag information.
    :rtype: AddTagToPhoto
    """
    image = await get_photo_by_id(image_id, db)

    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

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
