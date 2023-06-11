from domain.userinfo import UserInfo
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status, Depends
from .db_tables import UserDataBase
from .db import get_db
from service.hashing import verify_hashed_password, hash_password


def create_user(user: UserInfo, database: Session = next(get_db())):
    try:
        new_user = UserDataBase(login=user.login, password=hash_password(user.password))
        database.add(new_user)
        database.commit()
        database.refresh(new_user)
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Login {user.login} is already in use")
    return user



def check_password(user_for_checking: UserInfo, database: Session =next(get_db())):
    user = database.query(UserDataBase).filter(
        UserDataBase.email == user_for_checking.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")
    if not verify_hashed_password(user.password, user_for_checking.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")

    return user

def get_current_user_by_id(user_id: id, database: Session = next(get_db())):
    user = database.query(UserDataBase).filter(
        UserDataBase.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")

    return user