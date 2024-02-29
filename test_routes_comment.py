from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.entity.models import Comment, User
from src.repository.comments import create_comment, update_comment, delete_comment
from src.routes.comments_routes import router
from main import app

client = TestClient(app)

@pytest.fixture
def db():
    return Mock(Session)

@pytest.mark.asyncio
async def test_create_comment(db):
    user = User(id=1)  # Создаем пользователя для теста
    comment_data = {"comment": "Test comment"}
    image_id = 1

    response = client.post("/comments/", json={"comment_data": comment_data, "image_id": image_id})

    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["comment"] == comment_data["comment"]
    assert data["image_id"] == image_id
    assert data["user_id"] == user.id

@pytest.mark.asyncio
async def test_update_comment(db):
    user = User(id=1)
    comment_id = 1
    comment_data = {"comment": "Updated comment"}

    response = client.put(f"/comments/{comment_id}/update", json={"comment": comment_data})

    assert response.status_code == 201
    data = response.json()
    assert data["comment"] == comment_data["comment"]
    assert data["user_id"] == user.id

@pytest.mark.asyncio
async def test_delete_comment(db):
    user = User(id=1)
    comment_id = 1

    response = client.delete(f"/comments/{comment_id}")

    assert response.status_code == 201
    data = response.json()
    assert data["id"] == comment_id


if __name__ == '__main__':
    pytest.main()