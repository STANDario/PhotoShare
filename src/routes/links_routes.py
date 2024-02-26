from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.entity.models import ImageLink
from src.repository.image_link import create_image_link
from src.schemas import ImageLinkCreate
from src.utils.qrcode import generate_qr_code  

router = APIRouter()

@router.post("/image_links/", response_model=ImageLink)
async def create_image_link(image_link: ImageLinkCreate, db: AsyncSession = Depends(get_db)):
    db_image_link = await create_image_link(db=db, image_link=image_link)
    
   
    base_url = "https://yourserver.com"  
    image_url = f"{base_url}/images/{db_image_link.id}"  
    

    db_image_link.image_url = image_url
    
   
    await db.commit()
    await db.refresh(db_image_link)
    
   
    qr_code_path = f"qr_codes/{db_image_link.id}.png"  # Шлях до файлу QR-коду
    generate_qr_code(image_url, qr_code_path)  # Генеруємо QR-код для URL зображення
    db_image_link.qr_code_url = qr_code_path  # Зберігаємо шлях до QR-коду в базі даних
    

    await db.commit()
    await db.refresh(db_image_link)
    
    return db_image_link
