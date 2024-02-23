from pydantic import BaseModel


class ImageModel(BaseModel):
    id: int
    url: str
    description: str
    public_id: str


class ImageURLResponse(BaseModel):
    url: str
    description: str


class ImageDescResponse(BaseModel):
    id: int
    url: str
    description: str


class ImageUpdateResponse(BaseModel):
    id: int
    description: str


class ImageDeleteModel(BaseModel):
    id: int
    detail: str = "Image has been deleted"
