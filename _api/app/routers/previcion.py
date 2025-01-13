from fastapi import Depends, APIRouter, HTTPException, status
from typing import Union, Annotated
from .._schemas.user import RequestUserCreate, RequestUser
from .._models.user import User
from .._view import previcion
from ..database import get_db
from .._view.auth import is_user_autenticate
from sqlalchemy.orm import Session
from datetime import date, datetime
router = APIRouter()

@router.post("/api/previciones")
async def get_previcion(fecha_inicio:date, fecha_final:date,tipo:int, cultivo:int,   is_autenticate: Annotated[bool, Depends(is_user_autenticate)], db: Session = Depends(get_db)):
    return previcion.get_previcion(db, fecha_inicio, fecha_final, tipo, cultivo)

@router.post("/api/previcion")
async def get_previcion_by_day(tipo:int, cultivo:int, dia:str, is_autenticate: Annotated[bool, Depends(is_user_autenticate)], db: Session = Depends(get_db), ):
    return previcion.get_previcion_by_day(db, dia, tipo, cultivo)

@router.post("/api/previcion/semana")
async def get_previcion_semana(fecha_inicio: datetime, db: Session = Depends(get_db), ):
    return previcion.get_previcion_semana(db, fecha_inicio)

@router.get("/api/start-previcion")
async def get_previcion_by_day(db: Session = Depends(get_db), ):
    return previcion.start_predict(db)