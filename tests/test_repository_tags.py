from unittest.mock import MagicMock

import pytest
from sqlalchemy.orm import Session
from src.entity.models import Tag
from src.schemas.tag_schemas import TagModel
from src.repository.tags import (
    tag_create, get_tag_by_id, get_tag_by_name, get_tags, update_tag, remove_tag_by_name
)


@pytest.fixture
def db():
    return MagicMock(spec=Session)


@pytest.mark.asyncio
async def test_tag_create(db):
    body = TagModel(tag_name="Test Tag")
    result = await tag_create(body, db)
    assert result.tag_name == "test tag"


@pytest.mark.asyncio
async def test_get_tag_by_id(db):
    tag = Tag()
    db.execute().scalar.return_value = tag
    result = await get_tag_by_id(tag.id, db)
    assert result.id == tag.id


@pytest.mark.asyncio
async def test_get_tag_by_name(db):
    tag = Tag(tag_name="Test Tag")
    db.execute().scalar.return_value = tag
    result = await get_tag_by_name(tag.tag_name, db)
    assert result.tag_name == "Test Tag"


@pytest.mark.asyncio
async def test_get_tags(db):
    tags = [Tag(), Tag(), Tag()]
    db.execute().scalars().all.return_value = tags
    result = await get_tags(db)
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_update_tag(db):
    tag = Tag()
    db.execute().scalar.return_value = tag
    body = TagModel(tag_name="Updated Tag")
    result = await update_tag(tag.id, body, db)
    assert result.tag_name == "updated tag"


@pytest.mark.asyncio
async def test_remove_tag_by_name(db):
    tag = Tag(tag_name="Test Tag")
    db.execute().scalar.return_value = tag
    result = await remove_tag_by_name(tag.tag_name, db)
    assert result.tag_name == tag.tag_name
