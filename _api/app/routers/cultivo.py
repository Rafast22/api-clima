from fastapi import Depends, APIRouter, HTTPException, status
from typing import Union, Annotated
from .._schemas.cultivo import RequestCultivo, RequestCultivoCreate
from .._view.cultivo import update, get_by_id, delete_cultivo, get_by_user_id, create
from ..database import get_db
from .._view.auth import is_user_autenticate, get_current_user
from sqlalchemy.orm import Session


router = APIRouter()

@router.post("/api/user/cultivo")
async def create_localidad(cultivo: RequestCultivoCreate, is_autenticate: Annotated[bool, Depends(is_user_autenticate)], db: Session = Depends(get_db)):
    create(db, cultivo)

@router.put("/api/user/cultivo")
async def put_user(user: Annotated[RequestCultivo, Depends()], is_autenticate: Annotated[bool, Depends(is_user_autenticate)], db: Session = Depends(get_db)):
    return update(db, user)
    
@router.get("/api/user/cultivo/{cultivo_id}")
async def get_user(cultivo_id: int, is_autenticate: Annotated[bool, Depends(is_user_autenticate)], db: Session = Depends(get_db)):
    return get_by_id(db, cultivo_id)

@router.get("/api/user/cultivo/{user_id}")
async def get_user(user_id: int, is_autenticate: Annotated[bool, Depends(is_user_autenticate)], db: Session = Depends(get_db)):
    return get_by_user_id(db, user_id)
    

@router.delete("/api/user/cultivo/{cultivo_id}")
async def get_user(cultivo_id: int, is_autenticate: Annotated[bool, Depends(is_user_autenticate)], db: Session = Depends(get_db)):
    delete_cultivo(db, cultivo_id)
    
# @router.get("/users/me", response_model=None)
# async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
#     return current_user
