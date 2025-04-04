from .._models.user import User
from .._schemas.user import RequestUserResponse, RequestUserUpdate
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends


def update_user(db: Session , u: RequestUserUpdate):

    db_user = User.get(db, u.id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if User.get_user_by_email(db, u.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="{'error':'email already used'}")
    if User.get_user_by_username(db, u.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="{'error':'user already used'}")

    
    u.password = User.get_password_hash(u.password)
    db_user = User.update(db_user, db, u)
    
    return db_user

def get_user_by_id(db: Session, user_id:int ) -> RequestUserResponse:
    db_user = User.get(db, user_id)    
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return db_user

def delete_user_by_id(db: Session, user_id:int ):
    db_user = User.get(db, user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    User.delete(db_user, db)
        
       
