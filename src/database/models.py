from sqlalchemy import Column, Integer, String, func
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True)
    url_original = Column(String(255), nullable=False)
    url_transformed = Column(String(255), nullable=True)
    description = Column(String(255), nullable=True)
    created_at = Column('crated_at', DateTime, default=func.now())
    updated_at = Column('updated_at', DateTime)

    def json(self):
        return {
            "id": self.id,
            "url_original": self.url_original,
            "url_transformed": self.url_transformed,
            "description": self.description,
            "created_at": self.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%dT%H:%M:%S")
        }
