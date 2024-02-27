from sqlalchemy import Column, Integer, String, func, DateTime, ForeignKey, Table, Enum, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()


image_m2m_tag = Table(
    "image_m2m_tag",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("image_id", Integer, ForeignKey("images.id", ondelete="CASCADE")),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE")),
)


class Role(enum.Enum):
    user = "user"
    moderator = "moderator"
    admin = "admin"



class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    first_name = Column(String(25), nullable=True)
    last_name = Column(String(25), nullable=True)
    email = Column(String(50), nullable=False, unique=True)
    sex = Column(String(10), nullable=True)
    password = Column(String(150), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    refresh_token = Column(String(255))
    confirmed = Column(Boolean, default=False)
    role = Column(Enum(Role), default=Role.user)
    images = relationship("Image", backref="users")
    # ratings = relationship("Rating", backref="user")
    avatar = Column(String(255), nullable=True)

class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True)
    url = Column(String(255), nullable=False)
    public_id = Column(String(150))
    description = Column(String(150))
    created_at = Column("created_at", DateTime, default=func.now())
    updated_at = Column("updated_at", DateTime, default=func.now(), onupdate=func.now())
    tags = relationship("Tag", secondary=image_m2m_tag, back_populates="images")


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    tag_name = Column(String(13), nullable=False, unique=True)
    images = relationship("Image", secondary=image_m2m_tag, back_populates="tags")
