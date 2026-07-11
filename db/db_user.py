from fastapi import HTTPException,status
from sqlalchemy.orm.session import Session
from db.models import DbUser
from routers.schemas import UserBase
from db.hashing import Hash

def create_an_user(db: Session, user: UserBase):
    db_user = DbUser(
        username=user.username,
        email=user.email,
        password=Hash.bcrypt(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    exist = db.query(DbUser).filter(DbUser.username == username).first()
    if not exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return exist
