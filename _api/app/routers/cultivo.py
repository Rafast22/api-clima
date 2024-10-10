from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from typing import Union, Annotated
from .._schemas.user import RequestUserCreate, RequestUser
from .._models.auth import decode_token
from .._models.user import User
from .._view.cultivo import update, get_by_id, delete_cultivo, get_by_user_id
from ..database import oauth2_scheme
from ..database import get_db
from .._view.auth import is_user_autenticate, get_current_user
from sqlalchemy.orm import Session


router = APIRouter()

@router.put("/user/cultivo")
async def put_user(user: Annotated[RequestUser, Depends()], is_autenticate: Annotated[bool, Depends(is_user_autenticate)], db: Session = Depends(get_db)):
    return update(db, is_autenticate, user)
    
@router.get("/user/cultivo/{cultivo_id}")
async def get_user(cultivo_id: int, is_autenticate: Annotated[bool, Depends(is_user_autenticate)], db: Session = Depends(get_db)):
    return get_by_id(db, cultivo_id)

@router.get("/user/cultivo/{user_id}")
async def get_user(user_id: int, is_autenticate: Annotated[bool, Depends(is_user_autenticate)], db: Session = Depends(get_db)):
    return get_by_user_id(db, user_id)
    

@router.delete("/user/cultivo/{cultivo_id}")
async def get_user(cultivo_id: int, is_autenticate: Annotated[bool, Depends(is_user_autenticate)], db: Session = Depends(get_db)):
    delete_cultivo(db, cultivo_id)
    
# @router.get("/users/me", response_model=None)
# async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
#     return current_user
