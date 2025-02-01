
from .._models import cultivo
from .._schemas.cultivo import RequestCultivo, RequestCultivoCreate
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List

def update_cultivo(db: Session, u: RequestCultivo):

    try:
        db_cultivo = cultivo.get_cultivo_by_id(db, u.id)
        if not db_cultivo:
            raise HTTPException()
        # db_cultivo = cultivo.update_cultivo(db, u)
        cultivo.update_cultivo(db, u)
    except HTTPException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))

def get_cultivo_by_id(db: Session, cultivo_id:int ) -> RequestCultivo:
    '''Returns a Cultivo from the id'''
    db_cultivo = cultivo.get_cultivo_by_id(db, cultivo_id)
    if not db_cultivo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return db_cultivo

def delete_cultivo_by_id(db: Session, cultivo_id:int ):
    '''delete a cultivo by id'''
    db_cultivo = cultivo.get_cultivo_by_id(db, cultivo_id)
    if not db_cultivo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)    
    try:
        cultivo.delete_cultivo(db, cultivo_id)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))
        
def get_cultivos_by_user_id(db: Session, user_id:int ) -> List[RequestCultivo]:
    try:
        db_cultivo = cultivo.get_cultivos_usuario(db, user_id)
        if not db_cultivo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))
 
    return db_cultivo

def create_cultivo(db: Session, u: RequestCultivoCreate):
    try:
        cultivo.create_cultivo(db, u)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))


