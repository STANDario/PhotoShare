from sqlalchemy.ext.asyncio import AsyncSession
from src.entity.models import ImageLink
from src.schemas import ImageLinkCreate

async def create_image_link(db: AsyncSession, image_link: ImageLinkCreate):
    db_image_link = ImageLink(**image_link.dict())
    db.add(db_image_link)
    await db.commit()
    await db.refresh(db_image_link)
    return db_image_link

