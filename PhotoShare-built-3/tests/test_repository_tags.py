from unittest.mock import Mock

import pytest
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from src.entity.models import Tag
from src.schemas.tag_schemas import TagModel
from src.repository.tags import (
    tag_create, get_tag_by_id, get_tag_by_name, get_tags, update_tag, remove_tag_by_name
)

@pytest.fixture
def db():
    return Mock(Session)

@pytest.mark.asyncio
async def test_tag_create(db):
    body = TagModel(tag_name="Test Tag")
    result = await tag_create(body, db)
    assert result.tag_name == "test tag"  # Проверка ожидаемого поведения

@pytest.mark.asyncio
async def test_get_tag_by_id(db):
    tag_id = 1
    result = await get_tag_by_id(tag_id, db)
    assert result is None  # Проверка ожидаемого поведения

@pytest.mark.asyncio
async def test_get_tag_by_name(db):
    tag_name = "Test Tag"
    result = await get_tag_by_name(tag_name, db)
    assert result is None  # Проверка ожидаемого поведения

@pytest.mark.asyncio
async def test_get_tags(db):
    result = await get_tags(db)
    assert isinstance(result, list)  # Проверка ожидаемого типа результата

@pytest.mark.asyncio
async def test_update_tag(db):
    tag_id = 1
    body = TagModel(tag_name="Updated Tag")
    result = await update_tag(tag_id, body, db)
    assert result is None  # Проверка ожидаемого поведения

@pytest.mark.asyncio
async def test_remove_tag_by_name(db):
    tag_name = "Test Tag"
    result = await remove_tag_by_name(tag_name, db)
    assert result is None  # Проверка ожидаемого поведения

if __name__ == '__main__':
    pytest.main()