from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.comment_service import schemas, models
from app.db.database import get_db
from app.auth_service.security import get_current_auth_user
from app.auth_service import models as auth_models
from app.post_service.models import Post

router = APIRouter(prefix="/comments", tags=["Comments"])

@router.get("/post/{post_id}", response_model=list[schemas.Comment])
def get_comments_for_post(post_id: int, db: Session = Depends(get_db)):
    return db.query(models.Comment).where(models.Comment.post_id == post_id).all()

@router.post("/post/{post_id}", response_model=schemas.Comment)
def create_comment_for_post(
    post_id: int,
    comment_data: schemas.CommentCreate,
    db: Session = Depends(get_db),
    current_user: auth_models.User = Depends(get_current_auth_user)
):
    post = db.get(Post, post_id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    if comment_data.parent_id:
        parent = db.get(models.Comment, comment_data.parent_id)
        if not parent or parent.post_id != post_id:
            raise HTTPException(status_code=400, detail="Invalid parent comment")


    comment = models.Comment(
        content=comment_data.content,
        post_id=post.id,
        user_id=current_user.id,
        parent_id = comment_data.parent_id
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


@router.put("/{comment_id}", response_model=schemas.Comment)
def update_comment(
    comment_id: int,
    comment_data: schemas.CommentCreate,
    db: Session = Depends(get_db),
    current_user: auth_models.User = Depends(get_current_auth_user)
):

    comment = get_comment_by_user(comment_id, db, current_user)

    comment.content = comment_data.content
    db.commit()
    db.refresh(comment)
    return comment


@router.delete("/comment_id", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int,
   db: Session = Depends(get_db),
   current_user: auth_models.User = Depends(get_current_auth_user)
):
    comment = get_comment_by_user(comment_id, db, current_user)

    db.delete(comment)
    db.commit()


def get_comment_by_user(comment_id:int, db: Session, current_user: auth_models.User) -> models.Comment:
    comment = db.get(models.Comment, comment_id)

    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    if not comment.user_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your comment")

    return comment