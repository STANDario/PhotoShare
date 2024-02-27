import contextlib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.conf.config import settings, config
from src.utils import messages

SQLALCHEMY_DATABASE_URL = settings.sqlalchemy_database_url
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)




class DatabaseSessionManager:
    def __init__(self, url: str):
        self._engine: engine | None = create_engine(url)
        self._session_maker:sessionmaker = sessionmaker(autoflush=False, autocommit=False,
                                                                     bind=self._engine)

    @contextlib.asynccontextmanager
    async def session(self):
        if self._session_maker is None:
            raise Exception(messages.SESSION_NOT_INITIALIZED)
        session = self._session_maker()
        try:
            yield session
        except Exception as err:
            print(err)
            await session.rollback()
        finally:
            await session.close()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
