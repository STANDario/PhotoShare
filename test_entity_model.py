import pytest
import enum
from src.entity.models import Role, User, Image, Tag, Comment

def test_role_enum_values():
    assert Role.user == "user"
    assert Role.moderator == "moderator"
    assert Role.admin == "admin"

def test_create_user_instance():
    user = User(username="test_user", email="test@example.com", password="password")
    assert user.username == "test_user"
    assert user.email == "test@example.com"
    assert user.password == "password"
    assert user.role == Role.user

def test_create_image_instance():
    image = Image(url="http://example.com/image.jpg", description="Test image")
    assert image.url == "http://example.com/image.jpg"
    assert image.description == "Test image"

def test_create_tag_instance():
    tag = Tag(tag_name="Nature")
    assert tag.tag_name == "Nature"

def test_create_comment_instance():
    comment = Comment(comment="Great photo!")
    assert comment.comment == "Great photo!"

def test_update_user_role():
    user = User(username="test_user", email="test@example.com", password="password")
    user.role = Role.admin
    assert user.role == Role.admin

def test_image_tags_relationship():
    image = Image(url="http://example.com/image.jpg", description="Test image")
    tag = Tag(tag_name="Nature")
    image.tags.append(tag)
    assert tag in image.tags

# Добавьте другие тесты по аналогии для проверки различных сценариев

if __name__ == '__main__':
    pytest.main()