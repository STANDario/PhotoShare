from fastapi import HTTPException, status

from sqlalchemy.orm import Session
from src.schemas.link_schemas import ImageTransformModel, ImageLinkQR

from src.entity.models import Image, User
from src.utils.qrcode import generate_qr_code
from src.services.cloudinary_service import CloudImage


async def create_qr(body: ImageTransformModel, db: Session, user: User):
    """
    Generate a QR code for an image and associate it with the image.

    Args:
        body (ImageTransformModel): Data model containing information about the image.
        db (Session): Database session.
        user (User): Currently authenticated user.

    Raises:
        HTTPException: If the image is not found in the database.

    Returns:
        ImageLinkQR: Information about the generated QR code and its associated image.
    """
    
    image = db.query(Image).filter(Image.id == body.id).first()

    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

    if image.qr_url:
        return ImageLinkQR(image_id=image.id, qr_code_url=image.qr_url)

    qr_code_img = generate_qr_code(image.url)

    new_public_id = CloudImage.generate_name_image(user.email)

    upload_file = CloudImage.upload_image(qr_code_img, new_public_id)

    qr_code_url = CloudImage.get_url_for_image(new_public_id, upload_file)

    image.qr_url = qr_code_url

    db.commit()
    db.refresh(image)

    return ImageLinkQR(image_id=image.id, qr_code_url=qr_code_url)
