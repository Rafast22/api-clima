from fastapi import Depends, APIRouter, HTTPException, status
from typing import Union, Annotated
from .._schemas.user import RequestUserCreate, RequestUser
from .._models.user import User
from .._view import historico
from ..database import get_db
from .._view.auth import is_user_autenticate
from sqlalchemy.orm import Session
router = APIRouter()

@router.get("/historico/{user_id}")
async def get_historico_by_usuario(user_id: int, is_autenticate: Annotated[bool, Depends(is_user_autenticate)], db: Session = Depends(get_db)):
    return historico.get_historico_by_usuario(db, user_id)
