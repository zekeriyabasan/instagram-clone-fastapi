import random
import shutil
import string

from fastapi import APIRouter, Depends, HTTPException, UploadFile,status
from fastapi.params import File
from sqlalchemy.orm import Session

from auth.oauth2 import get_current_user
from db.database import get_db
from db import db_post
from routers.schemas import PostBase, PostDisplay, UserAuth

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    responses={404: {"description": "Not found"}},
)

image_url_types = ["absolute", "relative"]
@router.post("/", response_model=PostDisplay)
def create_post(post: PostBase, db: Session = Depends(get_db), current_user:UserAuth = Depends(get_current_user)): # current_user ile jwt validation yapıyoruz ve sadece login olan kullanıcı post oluşturabilir.
    if(not post.image_url_type in image_url_types):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=f"Invalid image_url_type. Must be one of {image_url_types}")
    return db_post.create_a_post(db, post, post.user_id) 
    
@router.get("/", response_model=list[PostDisplay])
def get_posts(db: Session = Depends(get_db),current_user:UserAuth = Depends(get_current_user)):
    return db_post.get_all_posts(db)

@router.post("/upload_image")
def upload_image(image: UploadFile = File(...), current_user:UserAuth = Depends(get_current_user)):
    # Save the uploaded image to a specific location
    letters = string.ascii_letters
    random_string = ''.join(random.choice(letters) for i in range(10))
    image.filename = f"{random_string}_{image.filename}"

    file_location = f"images/{image.filename}"
    with open(file_location, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer)
    return {"image_url": file_location}

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db), current_user:UserAuth = Depends(get_current_user)):
    post = db_post.get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to delete this post")
    db_post.delete_a_post(db, post_id)
    return {"detail": f"Post with id {post_id} deleted successfully"}

