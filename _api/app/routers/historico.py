from fastapi import Depends, APIRouter, HTTPException, status
from typing import Union, Annotated
from .._schemas.user import RequestUserCreate
from .._models.user import User
from .._view import historico
from ..database import get_db
from .._view.auth.auth import is_user_autenticate
from sqlalchemy.orm import Session
router = APIRouter()

@router.get("/api/historico")
async def get_historico_by_usuario(tipo:int, cultivo:int, is_autenticate: Annotated[bool, Depends(is_user_autenticate)], db: Session = Depends(get_db)):
    return historico.get_historico_by_usuario(db, tipo, cultivo)

@router.post("/api/historico")
async def get_historico_by_usuario_day(tipo:int, cultivo:int, dia:str, is_autenticate: Annotated[bool, Depends(is_user_autenticate)], db: Session = Depends(get_db), ):
    return historico.get_historico_by_usuario_day(db, dia, cultivo, tipo)

