from .._models import localidad, nasa_data
from .._models.user import get_by_id as get_user_by_id
from .._models.cultivo import get_cultivo_by_id
import asyncio
from .._schemas.localicad import RequestLocalidad, RequestLocalidadCreate
from .._schemas.nasa_data import RequestDataCreate
from sqlalchemy.orm import Session
from ..interceptor.nasa_request import get_history_date
from fastapi import HTTPException, status, Depends

def update_localidad(db: Session, u: RequestLocalidad) -> RequestLocalidad:

    try:
        db_localidad = localidad.get_by_id(db, u.id)
        if not db_localidad:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        db_localidad = localidad.update(db, u)
    except HTTPException:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))
    return db_localidad

def get_localidad_by_id(db: Session, localidad_id:int ) -> RequestLocalidad:
    try:
        db_localidad = localidad.get_by_id(db, localidad_id)
        if not db_localidad:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except HTTPException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))
    return db_localidad

def delete_localidad_by_id(db: Session, localidad_id:int ):
    try:
        db_localidad = localidad.get_by_id(db, localidad_id)
        if not db_localidad:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        localidad.delete(db, localidad_id)
    except HTTPException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))
        
def get_by_localidad_by_cultivo(db: Session, cultivo_id:int ) -> RequestLocalidad:
    try:
        db_localidad = localidad.get_by_cultivo_id(db, cultivo_id)
        if not db_localidad:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except HTTPException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))
    return db_localidad

def get_localidades_by_user_id(db: Session, cultivo_id:int ) -> RequestLocalidad:
    try:
        db_localidad = localidad.get_by_user_id(db, cultivo_id)
        if not db_localidad:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except HTTPException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except :
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return db_localidad

async def create_localidad(db: Session, u: RequestLocalidadCreate):
    try:
        history_data:list[RequestDataCreate] = await get_history_date(u.latitude, u.longitude)
        if u.user_id:
            user = get_user_by_id(db, u.user_id)
            if not user:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="'User' not found")
        if u.cultivo_id:
                    cultivo = get_cultivo_by_id(db, u.cultivo_id)
                    if not cultivo:
                        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="'Cultivo' not found")

        db_localidad = localidad.create(db, u)
        nasa_data.create_bulk(db, history_data,db_localidad.id)
    except HTTPException:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))
