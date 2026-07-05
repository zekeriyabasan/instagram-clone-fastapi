from sqlalchemy.orm.session import Session
from db.models import DbUser
from routers.schemas import UserBase


def create_an_user(db: Session, user: UserBase):
    db_user = DbUser(
        username=user.username,
        email=user.email,
        password=user.password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user