from fastapi import HTTPException, status

from sqlalchemy.orm import Session
from src.schemas.link_schemas import ImageTransformModel, ImageLinkQR

from src.entity.models import Image
from src.utils.qrcode import generate_qr_code
from src.services.cloudinary_service import CloudImage


async def create_qr(body: ImageTransformModel, db: Session):
    image = db.query(Image).filter(Image.id == body.id).first()

    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

    if image.qr_url:
        return ImageLinkQR(image_id=image.id, qr_code_url=image.qr_url)

    qr_code_img = generate_qr_code(image.url)

    new_public_id = CloudImage.generate_name_image()

    upload_file = CloudImage.upload_image(qr_code_img, new_public_id)

    qr_code_url = CloudImage.get_url_for_image(new_public_id, upload_file)

    image.qr_url = qr_code_url

    db.commit()
    db.refresh(image)

    return ImageLinkQR(image_id=image.id, qr_code_url=qr_code_url)
