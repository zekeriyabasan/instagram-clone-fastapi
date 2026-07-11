
from datetime import datetime

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