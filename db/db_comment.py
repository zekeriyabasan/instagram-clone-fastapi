
from datetime import datetime
from sqlalchemy.orm import Session

from db.models import DbComment
from routers.schemas import CommentBase
from datetime import datetime


def create_a_comment(db: Session, comment: CommentBase, user_id: int):
    db_comment = DbComment(
        content=comment.content,
        post_id=comment.post_id,
        user_id=user_id,
        timestamp=datetime.now()
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment