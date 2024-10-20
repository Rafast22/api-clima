import jwt
from typing import  Annotated
from jwt.exceptions import InvalidTokenError
from ..database import SECRET_KEY, ALGORITHM
from .._models.user import User
from ..database import oauth2_scheme
from .._models import user
from .._schemas.user import RequestUser, RequestUserCreate
from .._schemas.token import RequestToken, TokenData
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends


def update(db: Session , u: RequestUser) -> RequestUser:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Email or Username is registred",
        headers={"WWW-Authenticate": "Bearer"},
    )    

    db_user = user.get_user_by_email(db, u.email)
    if db_user is not None:
        raise credentials_exception
    
    u.password = User.get_password_hash(u.password)
    
    db_user = user.update_user(db, u)

    return db_user

    # if not db_user:
    #     raise HTTPException(status_code=404, detail="Usuário não encontrado")
    # return db_user

def get_by_id(db: Session, user_id:int ) -> RequestUser:
    db_user = user.get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user

def delete_user(db: Session, user_id:int ):
    try:
        user.delete_user(db, user_id)
        return {"ok": True}
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
        
       
