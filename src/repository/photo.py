from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import status, HTTPException

from src.entity.models import Image, Tag, User
from src.services.cloudinary_service import CloudImage
from src.schemas.photo_schemas import ImageChangeResponse, ImageModel
from src.schemas.tag_schemas import TagModel, AddTagToPhoto
from src.routes.tags_routes import create_tag


async def add_image(url: str, public_id: str, description: str, db: Session, user: User) -> Image | None:
    if not user:
        return None
    image = Image(url=url, public_id=public_id, user_id=user.id, description=description)
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


async def change_size_photo(image_id: int, width: int, db: Session, user: User):
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
        public_id=new_image.public_id
    )

    return ImageChangeResponse(image=image_model, detail="Image has been resized and added")


async def fade_edge_photo(image_id, db: Session, user: User):
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
        public_id=new_image.public_id
    )

    return ImageChangeResponse(image=image_model, detail="Image with fade effect has been added")


async def black_white_photo(image_id, db: Session, user: User):
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
        public_id=new_image.public_id
    )

    return ImageChangeResponse(image=image_model, detail="Image with fade effect has been added")


async def add_tag(image_id: int, tag_name: str, db: Session, user: User):
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
