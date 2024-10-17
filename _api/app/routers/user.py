from fastapi import Depends, APIRouter, HTTPException, status
from typing import Union, Annotated
from .._schemas.user import RequestUserCreate, RequestUser
from .._models.user import User
from .._view.user import update, get_by_id, delete_user
from ..database import get_db
from .._view.auth import is_user_autenticate
from sqlalchemy.orm import Session


router = APIRouter()

@router.put("/api/user")
async def put_user(user: Annotated[RequestUser, Depends()], is_autenticate: Annotated[bool, Depends(is_user_autenticate)], db: Session = Depends(get_db)):
    return update(db, is_autenticate, user)
    
@router.get("/api/user/{user_id}")
async def get_user(user_id: int, is_autenticate: Annotated[bool, Depends(is_user_autenticate)], db: Session = Depends(get_db)):
    return get_by_id(db, user_id)

@router.delete("/api/user/{user_id}")
async def get_user(user_id: int, is_autenticate: Annotated[bool, Depends(is_user_autenticate)], db: Session = Depends(get_db)):
    delete_user(db, user_id)
    
# @router.get("/users/me", response_model=None)
# async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
#     return current_user
