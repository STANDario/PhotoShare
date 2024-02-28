from datetime import datetime

from sqlalchemy.orm import Session

from src.entity.models import Comment, User
from src.schemas.comment_schemas import DeleteComment


async def create_comment(image_id: int, comment_data: str, db: Session, user: User):
    """
    Create a new comment associated with an image.

    Args:
        image_id (int): The ID of the image the comment is associated with.
        comment_data (str): The content of the comment.
        db (Session): Database session.
        user (User): User who is creating the comment.

    Returns:
        Comment: The newly created comment.
    """
    
    comment = Comment(comment=comment_data, image_id=image_id, user_id=user.id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


async def update_comment(comment_id: int, some_comment: str, db: Session, user: User):
    """
    Update an existing comment.

    Args:
        comment_id (int): The ID of the comment to be updated.
        some_comment (str): The updated content of the comment.
        db (Session): Database session.
        user (User): User who is updating the comment.

    Returns:
        Comment | None: The updated comment if successful, None otherwise.
    """
    comment = db.query(Comment).filter(Comment.id == comment_id).first()

    if user.role.name == "user" and comment.user_id != user.id:
        return None

    if comment:
        comment.comment = some_comment
        comment.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(comment)
        return comment
    else:
        return None


async def delete_comment(comment_id: int, db: Session, user: User):
    """
    Delete a comment.

    Args:
        comment_id (int): The ID of the comment to be deleted.
        db (Session): Database session.
        user (User): User who is deleting the comment.

    Returns:
        DeleteComment | None: Information about the deleted comment if successful, None otherwise.
    """
    comment = db.query(Comment).filter(Comment.id == comment_id).first()

    if not comment:
        return None

    if user.role.name == "user" and comment.user_id == user.id:
        return None

    if user.role.name == "admin" or user.role.name == "moderator":
        db.delete(comment)
        db.commit()
        return DeleteComment(id=comment.id, image_id=comment.image_id, comment=comment.comment)
