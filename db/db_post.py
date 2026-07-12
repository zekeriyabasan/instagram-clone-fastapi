
from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from db.models import DbPost
from routers.schemas import PostBase


def create_a_post(db: Session, post: PostBase, user_id: int):
    db_post = DbPost(
        title=post.title,
        content=post.content,
        image_url=post.image_url,
        image_url_type=post.image_url_type,
        user_id=user_id,
        timestamp=datetime.now()
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_all_posts(db: Session):
    return db.query(DbPost).all()

def get_post_by_id(db: Session, post_id: int):
    exist = db.query(DbPost).filter(DbPost.id == post_id).first()
    if not exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return exist

def delete_a_post(db: Session, post_id: int):
    db_post = db.query(DbPost).filter(DbPost.id == post_id).first()
    if db_post:
        db.delete(db_post)
        db.commit()
        return True
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")