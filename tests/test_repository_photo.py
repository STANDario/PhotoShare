from unittest.mock import MagicMock

import pytest
from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.entity.models import Image, User, Tag
from src.repository.photo import (
    add_image, get_photo_by_id, get_photo_by_desc, get_photo_all, update_photo,
    delete_photo, change_size_photo, fade_edge_photo, black_white_photo, add_tag
)


@pytest.fixture
def db():
    return MagicMock(spec=Session)


@pytest.mark.asyncio
async def test_add_image(db):
    user = User(id=1)
    result = await add_image("http://example.com/image.jpg", "12345", "Test Image", db, user)
    assert result.url == "http://example.com/image.jpg"


@pytest.mark.asyncio
async def test_get_photo_by_desc(db):
    photo = [Image(), Image(), Image()]
    db.query().filter().all.return_value = photo
    result = await get_photo_by_desc("Test Description", db)
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_get_photo_by_id(db):
    photo = Image()
    db.query().filter().first.return_value = photo
    result = await get_photo_by_id(1, db)
    assert photo.id == result.id


@pytest.mark.asyncio
async def test_get_photo_all(db):
    photo = [Image(), Image(), Image()]
    db.query().offset().limit().all.return_value = photo
    result = await get_photo_all(0, 10, db)
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_update_photo(db):
    photo = Image()
    db.query().filter().first.return_value = photo
    result = await update_photo(1, "Updated Description", db)
    assert result.description == "Updated Description"


@pytest.mark.asyncio
async def test_delete_photo(db):
    photo = Image(public_id="1")
    db.query().filter().first.return_value = photo
    result = await delete_photo(1, db)
    assert result.public_id == photo.public_id


@pytest.mark.asyncio
async def test_change_size_photo(db):
    user = User(id=1)
    with pytest.raises(HTTPException):
        await change_size_photo(1, 100, db, user)


@pytest.mark.asyncio
async def test_fade_edge_photo(db):
    user = User(id=1)
    with pytest.raises(HTTPException):
        await fade_edge_photo(1, db, user)


@pytest.mark.asyncio
async def test_black_white_photo(db):
    user = User(id=1)
    with pytest.raises(HTTPException):
        await black_white_photo(1, db, user)


# @pytest.mark.asyncio
# async def test_black_white_photo(db):
#     user = User(id=1)
#     image = Image(id=1, user_id=1, description="some desc")
#     db.query().filter().first.return_value = image
#
#     with patch("src.services.cloudinary_service.CloudImage.black_white") as mock_black_white:
#         with patch("src.schemas.photo_schemas.ImageModel") as mock_ImageModel:
#             mock_ImageModel.return_value = None
#
#             mock_black_white.return_value = ("mocked_url", "mocked_public_id")
#             result = await black_white_photo(image.id, db, user)
#
#             assert result.detail == "Image with black_white effect has been added"


@pytest.mark.asyncio
async def test_add_tag_not_found(db):
    db.query().filter().first.return_value = None
    user = User(id=1)
    with pytest.raises(HTTPException) as exc:
        await add_tag(1, "Test Tag", db, user)
    assert exc.value.detail == "Image not found"


@pytest.mark.asyncio
async def test_add_tag_not_user_id(db):
    image = Image(id=1, user_id=2)
    db.query().filter().first.return_value = image
    user = User(id=1)
    with pytest.raises(HTTPException) as exc:
        await add_tag(1, "Test Tag", db, user)
    assert exc.value.detail == "Can`t update someones picture"


@pytest.mark.asyncio
async def test_add_tag_over_five(db):
    image = Image(id=1, user_id=1, tags=[Tag(), Tag(), Tag(), Tag(), Tag()])
    db.query().filter().first.return_value = image
    user = User(id=1)
    with pytest.raises(HTTPException) as exc:
        await add_tag(1, "Test Tag", db, user)
    assert exc.value.detail == "Only five tags allowed"
