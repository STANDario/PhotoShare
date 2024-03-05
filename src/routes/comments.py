from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.entity.models import User
from src.repository.comments import create_comment, update_comment, delete_comment
from src.schemas.comment_schemas import CommentSchema, CommentsResponse, DeleteComment
from src.database.db import get_db
from src.services.auth_service import get_current_user
from src.services.role_service import admin_and_moder


router = APIRouter(prefix="/comments", tags=["comments"])


# Створюємо коментарі
@router.post("/", response_model=CommentsResponse, status_code=status.HTTP_201_CREATED)
async def create_comments(comment_data: CommentSchema, image_id: int, db: Session = Depends(get_db),
                          current_user: User = Depends(get_current_user)):
    """
    Create a new comment.

    Args:
        comment_data (CommentSchema): Comment data.
        image_id (int): Image ID.
        db (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (User, optional): Current user. Defaults to Depends(get_current_user).

    Returns:
        CommentsResponse: Created comment.
    """
    try:
        created_comment = await create_comment(image_id, comment_data.comment, db, current_user)
        return created_comment
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# Оновлюємо коментарі
@router.put("/{comment_id}/update", response_model=CommentsResponse, status_code=status.HTTP_201_CREATED)
async def update_comments(comment_id: int, comment: CommentSchema, db: Session = Depends(get_db),
                          current_user: User = Depends(get_current_user)):
    """
    Update a comment.

    Args:
        comment_id (int): Comment ID.
        comment (CommentSchema): Comment data.
        db (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (User, optional): Current user. Defaults to Depends(get_current_user).

    Returns:
        CommentsResponse: Updated comment.
    """
    updated_comment = await update_comment(comment_id, comment.comment, db, current_user)

    if updated_comment.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Can`t update someones comment")

    if updated_comment:
        return updated_comment
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")


# Видаляємо коментарі
@router.delete("/{comment_id}", response_model=DeleteComment, status_code=status.HTTP_201_CREATED,
               dependencies=[Depends(admin_and_moder)])
async def delete_comments(comment_id: int, db: Session = Depends(get_db),
                          current_user: User = Depends(get_current_user)):
    """
    Delete a comment.

    Args:
        comment_id (int): Comment ID.
        db (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (User, optional): Current user. Defaults to Depends(get_current_user).

    Returns:
        DeleteComment: Deleted comment.
    """
    deleted_comment = await delete_comment(comment_id, db, current_user)
    if deleted_comment:
        return deleted_comment
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
