from .._models.user import User
from .._models import user
from .._schemas.user import RequestUserResponse, RequestUserUpdate
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends


def update_user(db: Session , u: RequestUserUpdate) -> RequestUserUpdate:

    db_user = user.get_by_id(db, u.id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if user.get_user_by_email(db, u.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="{'error':'email already used'}")
    if user.get_user_by_username(db, u.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="{'error':'user already used'}")

    
    u.password = User.get_password_hash(u.password)
    db_user = user.update(db, u)
    
    return db_user

def get_user_by_id(db: Session, user_id:int ) -> RequestUserResponse:
    try:
        db_user = user.get_by_id(db, user_id)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))
    
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return db_user

def delete_user_by_id(db: Session, user_id:int ):
    db_user = user.get_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    try:
        user.delete(db, user_id)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))
        
       
