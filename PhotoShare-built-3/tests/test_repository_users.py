from unittest.mock import Mock, MagicMock

import pytest
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from libgravatar import Gravatar
from src.entity.models import User
from src.schemas.user_schemas import UserSchema
from src.repository.users import (
    get_user_by_email, get_user_by_username, create_user, update_token,
    confirmed_email, update_avatar_url, get_total_users_count
)

@pytest.fixture
def db():
    return Mock(Session)

@pytest.mark.asyncio
async def test_get_user_by_email(db):
    email = "test@example.com"
    result = await get_user_by_email(email, db)
    assert result is None  # Проверка ожидаемого поведения

@pytest.mark.asyncio
async def test_get_user_by_username(db):
    username = "test_user"
    result = await get_user_by_username(username, db)
    assert result is None  # Проверка ожидаемого поведения

@pytest.mark.asyncio
async def test_create_user(db):
    body = UserSchema()  # Создание действительного экземпляра UserSchema для тестирования
    result = await create_user(body, db)
    assert result is not None  # Проверка ожидаемого поведения

@pytest.mark.asyncio
async def test_update_token(db):
    user = Mock(User)
    token = "test_token"
    await update_token(user, token, db)
    # Добавить утверждения для проверки поведения функции

@pytest.mark.asyncio
async def test_confirmed_email(db):
    email = "test@example.com"
    await confirmed_email(email, db)
    # Добавить утверждения для проверки поведения функции


async def test_confirmed_email_notfound(db):
    email = "test@example.com"
    with db.assertRaises(ValueError):
        mocked_user = MagicMock()
        mocked_user.scalar_one_or_none.return_value = None
        db.session.execute.return_value = mocked_user
        await confirmed_email(email=email, db=db.session)

@pytest.mark.asyncio
async def test_update_avatar_url(db):
    email = "test@example.com"
    url = "http://example.com/avatar.jpg"
    result = await update_avatar_url(email, url, db)
    assert result.avatar == url  # Проверка ожидаемого поведения

@pytest.mark.asyncio
async def test_get_total_users_count(db):
    result = await get_total_users_count(db)
    assert isinstance(result, int)  # Проверка ожидаемого типа результата


if __name__ == '__main__':
    pytest.main()