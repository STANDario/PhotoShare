from typing import List

from pydantic import BaseModel

from src.schemas.tag_schemas import TagModel


class ImageModel(BaseModel):
    id: int
    url: str
    description: str
    public_id: str


class ImageURLResponse(BaseModel):
    url: str
    description: str
    tags: List[TagModel] | None


class ImageAllResponse(BaseModel):
    id: int
    url: str
    description: str
    tags: List[TagModel] | None


class ImageUpdateResponse(BaseModel):
    id: int
    description: str


class ImageDeleteModel(BaseModel):
    id: int
    detail: str = "Image has been deleted"


class ImageChangeResponse(BaseModel):
    image: ImageModel
    detail: str 