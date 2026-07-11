from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session

from db.database import get_db
from db import db_post
from routers.schemas import PostBase, PostDisplay

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    responses={404: {"description": "Not found"}},
)

image_url_types = ["absolute", "relative"]
@router.post("/", response_model=PostDisplay)
def create_post(post: PostBase, db: Session = Depends(get_db)):
    if(not post.image_url_type in image_url_types):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=f"Invalid image_url_type. Must be one of {image_url_types}")
    return db_post.create_a_post(db, post, post.user_id) 
    
@router.get("/", response_model=list[PostDisplay])
def get_posts(db: Session = Depends(get_db)):
    return db_post.get_all_posts(db)