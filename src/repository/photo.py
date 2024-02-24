from sqlalchemy.orm import Session
from fastapi import status, HTTPException

from src.entity.models import Image
from src.services.cloudinary_service import CloudImage
from src.schemas import ImageChangeSizeModel, ImageChangeResponse, ImageModel, ImageTransformModel


async def add_image(url: str, public_id: str, description: str, db: Session) -> Image | None:
    image = Image(url=url, public_id=public_id, description=description)
    db.add(image)
    db.commit()
    db.refresh(image)
    return image


async def get_photo_by_id(image_id: int, db: Session) -> Image | None:
    return db.query(Image).filter(Image.id == image_id).first()


async def get_photo_by_desc(description: str, db: Session):
    return db.query(Image).filter(Image.description.contains(description.lower())).all()


async def get_photo_all(db):
    return db.query(Image).filter().all()


async def update_photo(image_id: int, description: str, db: Session):
    image = await get_photo_by_id(image_id, db)
    if image:
        image.description = description
        db.commit()
    return image


async def delete_photo(image_id: int, db: Session):
    image = await get_photo_by_id(image_id, db)
    if image:
        CloudImage.delete_image(image.public_id)
        db.delete(image)
        db.commit()
    return image


async def change_size_photo(body: ImageChangeSizeModel, db: Session):
    image = await get_photo_by_id(body.id, db)

    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

    url, public_id = CloudImage.change_size(image.public_id, body.width)
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


async def fade_edge_photo(body: ImageTransformModel, db: Session):
    image = await get_photo_by_id(body.id, db)

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
