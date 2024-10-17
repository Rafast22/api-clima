from fastapi import Depends, APIRouter, HTTPException, status
from typing import Union, Annotated
from .._schemas.localicad import RequestLocalidad, RequestLocalidadCreate
from .._view.localidad import update, get_by_id, delete, get_by_cultivo_id, get_by_user_id, create
from ..database import get_db
from .._view.auth import is_user_autenticate
from sqlalchemy.orm import Session


router = APIRouter()

@router.put("/api/user/cultivo/localidad")
async def put_localidad(localidad: Annotated[RequestLocalidad, Depends()], is_autenticate: Annotated[bool, Depends(is_user_autenticate)], db: Session = Depends(get_db)):
    return await update(db, is_autenticate, localidad)
    
@router.get("/api/user/cultivo/localidad/{localidad_id}")
async def get_by_id(localidad_id: int, is_autenticate: Annotated[bool, Depends(is_user_autenticate)], db: Session = Depends(get_db)):
    return await get_by_id(db, localidad_id)

@router.get("/api/user/cultivo/localidad/cultivo/{cultivo_id}")
async def get_by_cultivo(cultivo_id: int, is_autenticate: Annotated[bool, Depends(is_user_autenticate)], db: Session = Depends(get_db)):
    return await get_by_cultivo_id(db, cultivo_id)
    
@router.get("/api/user/cultivo/localidad/user/{user_id}")
async def get_by_user(user_id: int, is_autenticate: Annotated[bool, Depends(is_user_autenticate)], db: Session = Depends(get_db)):
    return await get_by_user_id(db, user_id)
    
@router.delete("/api/user/cultivo/localidad/{localidad_id}")
async def delete_localidad(localidad_id: int, is_autenticate: Annotated[bool, Depends(is_user_autenticate)], db: Session = Depends(get_db)):
    await delete(db, localidad_id)
    
@router.post("/api/user/cultivo/localidad")
async def create_localidad(localidad: RequestLocalidadCreate, is_autenticate: Annotated[bool, Depends(is_user_autenticate)], db: Session = Depends(get_db)):
    await create(db, localidad)
    
@router.post("/api/user/cultivo/localidad_no_auth")
async def create_localidad_no_auth(localidad: Annotated[ RequestLocalidadCreate, Depends()], db: Session = Depends(get_db)):
    await create(db, localidad)
    
