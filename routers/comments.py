from fastapi import APIRouter, Depends, HTTPException, status
from routers.schemas import CommentBase
from auth.oauth2 import get_current_user
from db import db_comment, db_post
from sqlalchemy.orm import Session
from db.database import get_db
from routers.schemas import UserAuth

router = APIRouter(
    prefix="/comments",
    tags=["comments"],
    responses={404: {"description": "Not found"}}
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_comment(comment: CommentBase, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    post = db_post.get_post_by_id(db, comment.post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return db_comment.create_a_comment(db, comment, current_user.id)