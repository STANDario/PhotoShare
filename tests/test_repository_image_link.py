from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.repository.image_link import create_qr
from src.entity.models import Image, User
from src.schemas.link_schemas import ImageTransformModel


@pytest.fixture
def db():
    return MagicMock(spec=Session)


@pytest.mark.asyncio
async def test_create_qr_image_found(db):
    user = User(id=1, email="test@example.com")
    image = Image(id=1, url="http://example.com/image.jpg", qr_url=None)

    db.query().filter().first.return_value = image

    body = ImageTransformModel(id=1)
    result = await create_qr(body, db, user)

    assert result.image_id == 1
    assert result.qr_code_url is not None


@pytest.mark.asyncio
async def test_create_qr_image_not_found(db):
    user = User(id=1, email="test@example.com")

    db.query().filter().first.return_value = None

    body = ImageTransformModel(id=999)  # Image with ID 999 does not exist
    with pytest.raises(HTTPException) as exc_info:
        await create_qr(body, db, user)

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_create_qr_image_with_qr_url(db):
    user = User(id=1, email="test@example.com")
    image = Image(id=1, url="http://example.com/image.jpg", qr_url="http://example.com/qr_code.png")

    db.query().filter().first.return_value = image

    body = ImageTransformModel(id=1)
    result = await create_qr(body, db, user)

    assert result.image_id == 1
    assert result.qr_code_url == "http://example.com/qr_code.png"  # Убедимся, что qr_url не изменился


@pytest.mark.asyncio
async def test_create_qr_successful(db):
    user = User(id=1, email="test@example.com")
    image = Image(id=1, url="http://example.com/image.jpg", qr_url=None)

    db.query().filter().first.return_value = image

    body = ImageTransformModel(id=1)
    result = await create_qr(body, db, user)

    assert result.image_id == 1
    assert result.qr_code_url is not None
