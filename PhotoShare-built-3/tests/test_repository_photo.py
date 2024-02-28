from unittest.mock import Mock

import pytest
from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.entity.models import Image, User
from src.repository.photo import (
    add_image, get_photo_by_id, get_photo_by_desc, get_photo_all, update_photo,
    delete_photo, change_size_photo, fade_edge_photo, black_white_photo, add_tag
)

@pytest.fixture
def db():
    return Mock(Session)

@pytest.mark.asyncio
async def test_add_image(db):
    user = User(id=1)  # Подготовка пользователя для теста
    result = await add_image("http://example.com/image.jpg", "12345", "Test Image", db, user)
    assert result.url == "http://example.com/image.jpg"  # Проверка ожидаемого поведения

@pytest.mark.asyncio
async def test_get_photo_by_desc(db):
    result = await get_photo_by_desc("Test Description", db)
    assert isinstance(result, list)  # Проверка ожидаемого типа результата

@pytest.mark.asyncio
async def test_get_photo_all(db):
    result = await get_photo_all(0, 10, db)
    assert isinstance(result, list)  # Проверка ожидаемого типа результата

@pytest.mark.asyncio
async def test_update_photo(db):
    result = await update_photo(1, "Updated Description", db)
    assert result is None  # Проверка ожидаемого поведения

@pytest.mark.asyncio
async def test_delete_photo(db):
    result = await delete_photo(1, db)
    assert result is None  # Проверка ожидаемого поведения

@pytest.mark.asyncio
async def test_change_size_photo(db):
    user = User(id=1)  # Подготовка пользователя для теста
    with pytest.raises(HTTPException):
        await change_size_photo(1, 100, db, user)  # Проверка обработки исключения

        @pytest.mark.asyncio
        async def test_change_size_photo(db):
            user = User(id=1)  # Подготовка пользователя для теста
            with pytest.raises(HTTPException):
                await change_size_photo(1, 100, db, user)  # Проверка обработки исключения

        @pytest.mark.asyncio
        async def test_fade_edge_photo(db):
            user = User(id=1)  # Подготовка пользователя для теста
            with pytest.raises(HTTPException):
                await fade_edge_photo(1, db, user)  # Проверка обработки исключения

        @pytest.mark.asyncio
        async def test_black_white_photo(db):
            user = User(id=1)  # Подготовка пользователя для теста
            with pytest.raises(HTTPException):
                await black_white_photo(1, db, user)  # Проверка обработки исключения

        @pytest.mark.asyncio
        async def test_add_tag(db):
            user = User(id=1)  # Подготовка пользователя для теста
            with pytest.raises(HTTPException):
                await add_tag(1, "Test Tag", db, user)  # Проверка обработки исключения


if __name__ == '__main__':
    pytest.main()