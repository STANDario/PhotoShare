from unittest.mock import Mock

import pytest
from sqlalchemy.orm import Session
from src.entity.models import User, Role
from src.schemas.user_schemas import UserSchema
from src.repository.users import (
    get_user_by_email, get_user_by_username, create_user,
    update_avatar_url, get_total_users_count
)


@pytest.fixture
def db():
    return Mock(Session)


@pytest.mark.asyncio
async def test_get_user_by_email(db):
    user = User(email="test@example.com")
    db.execute().scalar_one_or_none.return_value = user
    result = await get_user_by_email(user.email, db)
    assert result.email == user.email


@pytest.mark.asyncio
async def test_get_user_by_username(db):
    user = User(username="test_user")
    db.execute().scalar_one_or_none.return_value = user
    username = "test_user"
    result = await get_user_by_username(username, db)
    assert result.username == "test_user"


@pytest.mark.asyncio
async def test_create_user(db):
    body = UserSchema(username="userame", email="deadpool@gmail.com", password="123456", first_name="first_name",
                      last_name="last_name", sex="male", role=Role.user)
    result = await create_user(body, db)
    assert result.username == body.username


@pytest.mark.asyncio
async def test_update_avatar_url(db):
    email = "test@example.com"
    url = "http://example.com/avatar.jpg"
    result = await update_avatar_url(email, url, db)
    assert result.avatar == url


@pytest.mark.asyncio
async def test_get_total_users_count(db):
    db.execute().scalar.return_value = 3
    result = await get_total_users_count(db)
    assert isinstance(result, int)
