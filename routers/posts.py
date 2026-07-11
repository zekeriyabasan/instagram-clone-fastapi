import random
import shutil
import string

from fastapi import APIRouter, Depends, HTTPException, UploadFile,status
from fastapi.params import File
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

@router.post("/upload_image")
def upload_image(image: UploadFile = File(...)):
    # Save the uploaded image to a specific location
    letters = string.ascii_letters
    random_string = ''.join(random.choice(letters) for i in range(10))
    image.filename = f"{random_string}_{image.filename}"

    file_location = f"images/{image.filename}"
    with open(file_location, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer)
    return {"info": f"Image '{image.filename}' uploaded successfully. path:{file_location}"}

