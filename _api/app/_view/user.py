from .._models.user import User
from .._models import user
from .._schemas.user import RequestUser
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends


def update_user(db: Session , u: RequestUser) -> RequestUser:

    try:
        db_user = user.get_user_by_email(db, u.email)
        if not db_user:
            raise HTTPException
        u.password = User.get_password_hash(u.password)
        db_user = user.update(db, u)
    except HTTPException as ex:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))
    
    return db_user

def get_user_by_id(db: Session, user_id:int ) -> RequestUser:
    try:
        db_user = user.get_by_id(db, user_id)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))
    
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return db_user

def delete_user_by_id(db: Session, user_id:int ):
    db_user = user.get_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    try:
        user.delete(db, user_id)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))
        
       
