from typing import List, Type

from sqlalchemy.future import select
from sqlalchemy.orm import Session

from src.entity.models import Tag
from src.schemas.tag_schemas import TagModel


async def tag_create(body: TagModel, db: Session) -> Tag:

    tag = Tag(tag_name=body.tag_name.lower())
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


async def get_tag_by_id(tag_id: int, db: Session) -> Tag | None:

    result = db.execute(select(Tag).filter(Tag.id == tag_id))
    tag = result.scalar()
    return tag


async def get_tag_by_name(tag_name: str, db: Session) -> Tag | None:

    result = db.execute(select(Tag).filter(Tag.tag_name == tag_name))
    tag = result.scalar()
    return tag


async def get_tags(db: Session) -> List[Type[Tag]]:

    result = db.execute(select(Tag))
    tags = result.scalars().all()
    return tags


async def update_tag(tag_id: int, body: TagModel, db: Session) -> Tag | None:

    result = db.execute(select(Tag).filter(Tag.id == tag_id))
    tag = result.scalar()
    if not tag:
        return None
    tag.tag_name = body.tag_name.lower()
    db.commit()
    return tag


async def remove_tag_by_name(tag_name: str, db: Session) -> Tag | None:

    result = db.execute(select(Tag).filter(Tag.tag_name == tag_name))
    tag = result.scalar()
    if tag:
        db.delete(tag)
        db.commit()
    return tag
