from typing import List, Type

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.entity.models import Tag, User
from src.repository import tags as repo_tags
from src.schemas.tag_schemas import TagModel, TagResponse
from src.services.auth_service import get_current_user
from src.services.role_service import admin_and_moder


router = APIRouter(prefix="/tags", tags=["tags"])


@router.post("/", response_model=TagResponse)
async def create_tag(body: TagModel, db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_user)) -> Tag | None:

    tag_exist = await repo_tags.get_tag_by_name(body.tag_name.lower(), db)
    if tag_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Tag already exists")
    tag = await repo_tags.tag_create(body, db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return tag


@router.get("/by_id/{tag_id}", response_model=TagResponse)
async def get_tag_by_id(tag_id: int, db: Session = Depends(get_db),
                        current_user: User = Depends(get_current_user)) -> Tag | None:

    tag = await repo_tags.get_tag_by_id(tag_id, db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid tag")
    return tag


@router.get("/by_name/{tag_name}", response_model=TagResponse)
async def get_tag_by_name(tag_name: str, db: Session = Depends(get_db),
                          current_user: User = Depends(get_current_user)) -> Tag | None:

    tag = await repo_tags.get_tag_by_name(tag_name, db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid tag")
    return tag


@router.get("/", response_model=List[TagResponse])
async def get_all_tags(db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user)) -> list[Type[Tag]] | None:

    tags = await repo_tags.get_tags(db)
    return tags


@router.patch("/{tag_id}", response_model=TagResponse)
async def update_tag(tag_id: int, body: TagModel, db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_user)) -> Tag | None:

    tag = await repo_tags.update_tag(tag_id, body, db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid tag")
    return tag


@router.delete("/", response_model=TagResponse, dependencies=[Depends(admin_and_moder)])
async def delete_tag(identifier: str, db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_user)) -> Tag | None:

    tag = await repo_tags.remove_tag_by_name(identifier, db)

    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid tag")
    return tag
