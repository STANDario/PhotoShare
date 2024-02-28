from datetime import datetime

from sqlalchemy.orm import Session

from src.entity.models import Comment
from src.schemas.comment_schemas import DeleteComment


async def create_comment(image_id: int, comment_data: str, db: Session):
    """
    Create a new comment.

    This function creates a new comment for the image with the specified ID.

    :param image_id: The ID of the image to add the comment to.
    :type image_id: int
    :param comment_data: The content of the comment.
    :type comment_data: str
    :param db: Database session.
    :type db: Session
    :return: The created comment.
    :rtype: Comment
    """
    comment = Comment(comment=comment_data, image_id=image_id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


async def update_comment(comment_id: int, some_comment: str, db: Session):
    """
    Update an existing comment.

    This function updates the content of the comment with the specified ID.

    :param comment_id: The ID of the comment to update.
    :type comment_id: int
    :param some_comment: The new content of the comment.
    :type some_comment: str
    :param db: Database session.
    :type db: Session
    :return: The updated comment if found, otherwise None.
    :rtype: Comment | None
    """
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
    """
    Delete a comment.

    This function deletes the comment with the specified ID.

    :param comment_id: The ID of the comment to delete.
    :type comment_id: int
    :param db: Database session.
    :type db: Session
    :return: The deleted comment if found, otherwise None.
    :rtype: DeleteComment | None
    """
    comment = db.query(Comment).filter(Comment.id == comment_id).first()

    if comment:
        db.delete(comment)
        db.commit()
        return DeleteComment(id=comment.id, image_id=comment.image_id, comment=comment.comment)
    else:
        return None
