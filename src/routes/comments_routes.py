from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.repository.comments import create_comment, update_comment, delete_comment
from src.schemas.comment_schemas import CommentSchema, CommentsResponse, DeleteComment
from src.database.db import get_db


router = APIRouter(prefix="/comments", tags=["comments"])


# Створюємо коментарі
@router.post("/", response_model=CommentsResponse, status_code=status.HTTP_201_CREATED)
async def create_comments(comment_data: CommentSchema, image_id: int, db: Session = Depends(get_db)):
    try:
        created_comment = await create_comment(image_id, comment_data.comment, db)
        return created_comment
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# Оновлюємо коментарі
@router.put("/{comment_id}/update", response_model=CommentsResponse, status_code=status.HTTP_201_CREATED)
async def update_comments(comment_id: int, comment: CommentSchema, db: Session = Depends(get_db)):
    updated_comment = await update_comment(comment_id, comment.comment, db)
    if updated_comment:
        return updated_comment
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")


# Видаляємо коментарі
@router.delete("/{comment_id}", response_model=DeleteComment, status_code=status.HTTP_201_CREATED)
async def delete_comments(comment_id: int, db: Session = Depends(get_db)):
    deleted_comment = await delete_comment(comment_id, db)
    if deleted_comment:
        return deleted_comment
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
