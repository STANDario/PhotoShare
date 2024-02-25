from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict


class TagModel(BaseModel):
    tag_name: str


class TagResponse(TagModel):
    model_config = SettingsConfigDict(from_attributes=True)
    id: int
    tag_name: str


class AddTag(BaseModel):
    detail: str = "Image tags has been updated"


class AddTagToPhoto(BaseModel):
    detail: str = "Tag successfully added to photo"
    tag: str