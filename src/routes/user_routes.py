import pickle

import cloudinary
import cloudinary.uploader
from fastapi import APIRouter, File, Depends, UploadFile
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas.user_schemas import UserResponse
from src.entity.models import User
from src.conf.config import settings
from src.services.auth_service import auth_service
from src.repository import users as repository_users


router = APIRouter(prefix='/users', tags=['users'])
cloudinary.config(cloud_name=settings.cloud_name, api_key=settings.api_key, api_secret=settings.api_secret, secure=True)


@router.get("/me", response_model=UserResponse,
            description='No more than 3 requests per minute',
            dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def get_current_user(user: User = Depends(auth_service.get_current_user)):

    return user


@router.patch("/avatar", response_model=UserResponse,
              description='No more than 3 requests per minute',
              dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def get_current_user(file: UploadFile = File(),
                           user: User = Depends(auth_service.get_current_user),
                           db: Session = Depends(get_db)):

    public_id = f"Contacts_Hw_web/{user.email}"
    res = cloudinary.uploader.upload(file.file, public_id=public_id, overwrite=True)
    res_url = cloudinary.CloudinaryImage(public_id).build_url(width=250, height=250, crop="fill",
                                                              version=res.get("version"))

    await repository_users.update_avatar_url(email=user.email, url=res_url, db=db)
    auth_service.cache.set(user.email, pickle.dumps(user))
    auth_service.cache.expire(user.email, 300)

    return user
