from sqlalchemy.orm import Session

from src.database.models import Image


async def get_p(db: Session, id: int):
    return db.query(Image).filter(Image.id == id).first()
