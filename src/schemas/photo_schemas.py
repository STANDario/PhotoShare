from typing import List

from pydantic import BaseModel

from src.schemas.tag_schemas import TagModel
from src.schemas.comment_schemas import CommentForPhotoSchema


class ImageModel(BaseModel):
    id: int
    url: str
    description: str
    public_id: str
    user_id: int


class ImageURLResponse(BaseModel):
    user_id: int
    url: str
    description: str
    qr_url: str | None
    tags: List[TagModel] | None
    comments: List[CommentForPhotoSchema] | None


class ImageAllResponse(BaseModel):
    id: int
    user_id: int
    url: str
    description: str
    qr_url: str | None
    tags: List[TagModel] | None
    comments: List[CommentForPhotoSchema] | None


class ImageUpdateResponse(BaseModel):
    id: int
    description: str


class ImageDeleteModel(BaseModel):
    id: int
    detail: str = "Image has been deleted"


class ImageChangeResponse(BaseModel):
    image: ImageModel
    detail: str 
