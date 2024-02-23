from sqlalchemy.orm import Session

from src.entity.models import Image
from src.services.cloudinary_service import CloudImage


async def add_image(url: str, public_id: str, description: str, db: Session) -> Image | None:
    image = Image(url=url, public_id=public_id, description=description)
    db.add(image)
    db.commit()
    db.refresh(image)
    return image


async def get_photo_by_id(image_id: int, db: Session) -> str | None:
    return db.query(Image).filter(Image.id == image_id).first()


async def get_photo_by_desc(description: str, db: Session):
    return db.query(Image).filter(Image.description.contains(description.lower())).all()


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
