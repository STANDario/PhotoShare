import asyncio

import pytest
import pytest_asyncio
import redis.asyncio as aioredis
from unittest.mock import MagicMock
from fastapi import FastAPI, Depends
from fastapi_limiter import FastAPILimiter
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from src.entity.models import Base, User
from src.database.db import get_db
from src.services.auth_service import auth_service


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

test_user = {"username": "agent007",
             "first_name": "andrii",
             "last_name": "drovorub",
             "sex": "male",
             "role": "admin",
             "email": "agent007@gmail.com",
             "password": "12345678"}


# @pytest.fixture(scope="module", autouse=True)
# def init_models_wrap():
#     def init_models():
#         with TestingSessionLocal() as session:
#             hash_password = auth_service.get_password_hash(test_user["password"])
#             current_user = User(username=test_user["username"], email=test_user["email"], password=hash_password,
#                                 confirmed=True, role="admin", avatar="127.0.0.1://my_avatar.jpg")
#             session.add(current_user)
#             session.commit()
#
#     init_models()


@pytest.fixture(scope="module")
def session():
    # Create the database
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def client(session):
    # Dependency override
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)


@pytest_asyncio.fixture()
async def get_token():
    access_token = await auth_service.create_access_token(data={"sub": test_user["email"], "DB-class": "PSQL"})
    refresh_token = await auth_service.create_refresh_token(data={"sub": test_user["email"]})
    return access_token, refresh_token


# @pytest.fixture
# def app_without_limiter():
#     app = FastAPI()
#
#     @app.on_event("startup")
#     async def startup_event():
#         pass
#
#     return app


if __name__ == '__main__':
    pytest.main()
