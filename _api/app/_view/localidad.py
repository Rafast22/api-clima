from .._models import localidad
from .._models.user import get_by_id as get_user_by_id
from .._models.cultivo import get_cultivo_by_id
import asyncio
from .._schemas.localidad import RequestLocalidad, RequestLocalidadCreate
from .._schemas.nasa_data import RequestDataCreate
from sqlalchemy.orm import Session
from ..interceptor.nasa_request import get_history_date
from ..interceptor import predict
from fastapi import HTTPException, status, BackgroundTasks

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

async def create_localidad(db: Session, local: RequestLocalidadCreate, background_tasks: BackgroundTasks):
    try:
        
        if local.user_id:
            user = get_user_by_id(db, local.user_id)
            if not user:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="'User' not found")
        if local.cultivo_id:
                    cultivo = get_cultivo_by_id(db, local.cultivo_id)
                    if not cultivo:
                        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="'Cultivo' not found")

        db_localidad = localidad.create(db, local)
        background_tasks.add_task(make_predictions, db, db_localidad)

        # nasa_data.create_bulk(db, history_data,db_localidad.id)
    except HTTPException:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))

async def make_predictions(db:Session, local:localidad.Localidad):
    try:
        data = await get_history_date(local.latitude, local.longitude)
        predict.predict(db , data, local)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))
