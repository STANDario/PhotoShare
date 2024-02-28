from pydantic import BaseModel


class ImageLinkQR(BaseModel):
    image_id: int
    qr_code_url: str


class ImageTransformModel(BaseModel):
    id: int
