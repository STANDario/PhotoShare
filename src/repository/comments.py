from datetime import datetime

from sqlalchemy.orm import Session

from src.entity.models import Comment
from src.schemas.comment_schemas import DeleteComment


async def create_comment(image_id: int, comment_data: str, db: Session):
    comment = Comment(comment=comment_data, image_id=image_id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


async def update_comment(comment_id: int, some_comment: str, db: Session):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()

    if comment:
        comment.comment = some_comment
        comment.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(comment)
        return comment
    else:
        return None


async def delete_comment(comment_id: int, db: Session):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()

    if comment:
        db.delete(comment)
        db.commit()
        return DeleteComment(id=comment.id, image_id=comment.image_id, comment=comment.comment)
    else:
        return None
