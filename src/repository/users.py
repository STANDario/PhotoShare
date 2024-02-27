from fastapi import Depends
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from src.schemas.user_schemas import UserSchema
from libgravatar import Gravatar

from src.database.db import get_db
from src.entity.models import User


async def get_user_by_email(email: str, db: Session = Depends(get_db)):

    stmt = select(User).filter_by(email=email)
    user = db.execute(stmt)
    user = user.scalar_one_or_none()
    return user


async def create_user(body: UserSchema, db: Session = Depends(get_db)):

    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as err:
        print(err)

    new_user = User(**body.model_dump(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session):

    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session):

    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar_url(email: str, url: str | None, db: Session) -> User:

    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    db.refresh(user)
    return user


async def get_total_users_count(db: Session):

    count = db.execute(select(func.count(User.id)))
    total_count = count.scalar()
    return total_count
