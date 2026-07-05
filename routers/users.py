from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_db
from db.db_user import create_an_user
from routers.schemas import UserBase, UserDisplay

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=UserDisplay)
def create_user(user: UserBase, db: Session = Depends(get_db)):
    return create_an_user(db, user) 
    