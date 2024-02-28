from unittest.mock import Mock

import pytest
from datetime import datetime

from _pytest.main import Session

from src.repository.comments import create_comment, update_comment, delete_comment
from src.entity.models import Comment, User

@pytest.fixture
def db():
    return Mock(Session)

@pytest.mark.asyncio
async def test_create_comment(db):
    user = User(id=1)
    image_id = 1
    comment_data = "Test comment"

    comment = await create_comment(image_id, comment_data, db, user)

    assert comment.comment == comment_data
    assert comment.image_id == image_id
    assert comment.user_id == user.id

@pytest.mark.asyncio
async def test_update_comment(db):
    user = User(id=1, role="user")
    comment_id = 1
    new_comment = "Updated comment"

    comment = Comment(id=comment_id, comment="Old comment", user_id=1)
    db.add(comment)
    db.commit()

    updated_comment = await update_comment(comment_id, new_comment, db, user)

    assert updated_comment.comment == new_comment
    assert updated_comment.updated_at is not None
    assert updated_comment.updated_at > comment.updated_at

@pytest.mark.asyncio
async def test_delete_comment(db):
    user = User(id=1, role="admin")
    comment_id = 1

    comment = Comment(id=comment_id, comment="Test comment", user_id=1)
    db.add(comment)
    db.commit()

    result = await delete_comment(comment_id, db, user)

    assert result is not None
    assert result.id == comment_id
    assert result.comment == "Test comment"

# Добавьте другие тесты по аналогии для различных сценариев

if __name__ == '__main__':
    pytest.main()