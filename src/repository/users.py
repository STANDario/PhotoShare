from sqlalchemy import select, func
from sqlalchemy.orm import Session
from libgravatar import Gravatar

from src.entity.models import User
from src.schemas.user_schemas import UserSchema


async def get_user_by_email(email: str, db: Session):
    """
    Retrieve a user by their email.

    Args:
        email (str): User email.
        db (Session): Database session.

    Returns:
        User: Retrieved user.
    """
    stmt = select(User).filter_by(email=email)
    user = db.execute(stmt)
    user = user.scalar_one_or_none()
    return user


async def get_user_by_username(username: str, db: Session):
    """
    Retrieve a user by their username.

    Args:
        username (str): User username.
        db (Session): Database session.

    Returns:
        User: Retrieved user.
    """
    stmt = select(User).filter_by(username=username)
    user = db.execute(stmt)
    user = user.scalar_one_or_none()
    return user


async def create_user(body: UserSchema, db: Session):
    """
    Create a new user.

    Args:
        body (UserSchema): User data.
        db (Session): Database session.

    Returns:
        User: Created user.
    """
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
    """
    Update user token.

    Args:
        user (User): User instance.
        token (str | None): Refresh token.
        db (Session): Database session.
    """
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session):
    """
    Confirm user email.

    Args:
        email (str): User email.
        db (Session): Database session.
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar_url(email: str, url: str | None, db: Session) -> User:
    """
    Update user avatar URL.

    Args:
        email (str): User email.
        url (str | None): Avatar URL.
        db (Session): Database session.

    Returns:
        User: Updated user.
    """ 
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    db.refresh(user)
    return user


async def get_total_users_count(db: Session):
    """
    Get total count of users.

    Args:
        db (Session): Database session.

    Returns:
        int: Total count of users.
    """
    count = db.execute(select(func.count(User.id)))
    total_count = count.scalar()
    return total_count
