
from .._models.cultivo import Cultivo
from .._models.user import User
from .._schemas.cultivo import RequestCultivo, RequestCultivoCreate
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List

def update_cultivo(db: Session, cultivo: RequestCultivo):

    db_cultivo = Cultivo.get(db, cultivo.id)
    if not db_cultivo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    Cultivo.update(db_cultivo, db, **cultivo.model_dump())

def get_cultivo_by_id(db: Session, cultivo_id:int ):
    db_cultivo = Cultivo.get(db, cultivo_id)
    if not db_cultivo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return db_cultivo

def delete_cultivo_by_id(db: Session, cultivo_id:int ):
    db_cultivo = Cultivo.get(db, cultivo_id)
    if not db_cultivo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)    
    Cultivo.delete(db_cultivo, db)
    
def get_cultivos_by_user_id(db: Session, user_id:int ):
    db_cultivo = Cultivo.get_cultivos_usuario(db, user_id)
    if not db_cultivo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return db_cultivo

def create_cultivo(db: Session, cultivo: RequestCultivoCreate, user:User):
    Cultivo.create(db, **cultivo.model_dump(), user_id=user.id)

