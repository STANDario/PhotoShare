from sqlalchemy import Column, Integer, String, func, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True)
    url = Column(String(255), nullable=False)
    public_id = Column(String(150))
    description = Column(String(150))
    created_at = Column("created_at", DateTime, default=func.now())
    updated_at = Column("updated_at", DateTime, default=func.now(), onupdate=func.now())
