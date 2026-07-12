from datetime import datetime

from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str
    password: str

    model_config = {
        "from_attributes": True
    }

class UserDisplay(BaseModel):
    username: str
    email: str

    model_config = {
        "from_attributes": True
    }

# User for Post Display Schema
class User(BaseModel):
    username: str

    model_config = {
        "from_attributes": True
    }

class PostBase(BaseModel):
    title: str
    content: str
    image_url: str 
    image_url_type: str
    user_id: int

    model_config = {
        "from_attributes": True
    }

class PostDisplay(BaseModel):
    title: str
    content: str
    image_url: str
    image_url_type: str
    user_id: int
    user: User
    timestamp: datetime

    model_config = {
        "from_attributes": True
    }

class UserAuth(BaseModel):
    id: int
    username: str
    email: str

class CommentBase(BaseModel):
    content: str
    post_id: int

    model_config = {
        "from_attributes": True
    }