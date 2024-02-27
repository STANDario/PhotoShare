from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.repository.image_link import create_qr
from src.schemas.link_schemas import ImageTransformModel, ImageLinkQR


router = APIRouter(prefix="/qr_code", tags=["qr_code"])


@router.post("/image_links/", response_model=ImageLinkQR)
async def create_image_link(body: ImageTransformModel, db: Session = Depends(get_db)):

    image = await create_qr(body, db)

    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

    return image
