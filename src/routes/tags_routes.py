from typing import List, Type

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.entity.models import Tag
from src.repository import tags as repo_tags
from src.schemas.tag_schemas import TagModel, TagResponse

router = APIRouter(prefix="/tags", tags=["tags"])


# Create a new tag
@router.post("/", response_model=TagResponse)
async def create_tag(body: TagModel, db: Session = Depends(get_db)) -> Tag | None:
    """
    Create a new tag.

    This endpoint creates a new tag using the provided data.

    :param body: Data to create the new tag.
    :type body: TagModel
    :param db: Database session.
    :type db: Session
    :return: Created tag.
    :rtype: Tag | None
    """


# Get a tag by its ID
@router.get("/by_id/{tag_id}", response_model=TagResponse)
async def get_tag_by_id(tag_id: int, db: Session = Depends(get_db)) -> Tag | None:
    """
    Retrieve a tag by its ID.

    This endpoint retrieves a tag based on the provided ID.

    :param tag_id: The ID of the tag to retrieve.
    :type tag_id: int
    :param db: Database session.
    :type db: Session
    :return: Retrieved tag.
    :rtype: Tag | None
    """


# Get a tag by its name
@router.get("/by_name/{tag_name}", response_model=TagResponse)
async def get_tag_by_name(tag_name: str, db: Session = Depends(get_db)) -> Tag | None:
    """
    Retrieve a tag by its name.

    This endpoint retrieves a tag based on the provided name.

    :param tag_name: The name of the tag to retrieve.
    :type tag_name: str
    :param db: Database session.
    :type db: Session
    :return: Retrieved tag.
    :rtype: Tag | None
    """


# Get all tags
@router.get("/", response_model=List[TagResponse])
async def get_all_tags(db: Session = Depends(get_db)) -> list[Type[Tag]] | None:
    """
    Retrieve all tags.

    This endpoint retrieves all tags from the database.

    :param db: Database session.
    :type db: Session
    :return: List of retrieved tags.
    :rtype: list[Type[Tag]] | None
    """


# Update a tag
@router.patch("/{tag_id}", response_model=TagResponse)
async def update_tag(tag_id: int, body: TagModel, db: Session = Depends(get_db)) -> Tag | None:
    """
    Update a tag.

    This endpoint updates a tag with the specified tag_id.

    :param tag_id: ID of the tag to be updated.
    :type tag_id: int
    :param body: TagModel containing the new tag information.
    :type body: TagModel
    :param db: Database session.
    :type db: Session
    :return: Updated tag.
    :rtype: Tag | None
    """


# Delete a tag
@router.delete("/", response_model=TagResponse)
async def delete_tag(identifier: str, db: Session = Depends(get_db)) -> Tag | None:
    """
    Delete a tag.

    This endpoint deletes a tag with the specified identifier.

    :param identifier: ID or name of the tag to be deleted.
    :type identifier: str
    :param db: Database session.
    :type db: Session
    :return: Deleted tag.
    :rtype: Tag | None
    """
