from .._models.localidad import Localidad 
from .._models.user import User
from .._models.cultivo import Cultivo
import asyncio
from .._schemas.localidad import RequestLocalidad, RequestLocalidadCreate
from .._schemas.nasa_data import RequestDataCreate
from sqlalchemy.orm import Session
from ..interceptor.nasa_request import get_history_date
from ..interceptor import predict
from fastapi import HTTPException, status, BackgroundTasks


async def create_localidad(db: Session, local: RequestLocalidadCreate, background_tasks: BackgroundTasks, user:User):
    db_localidad = Localidad.create(db, **local.model_dump(), user_id=user.id)
    background_tasks.add_task(make_predictions, db, db_localidad)

def update_localidad(db: Session, localidad: RequestLocalidad):
    db_localidad = Localidad.get(db, localidad.id)
    if not db_localidad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Localidad not found')
    db_localidad = Localidad.update(db_localidad, db, **localidad.model_dump())
    return db_localidad

def get_localidad_by_id(db: Session, localidad_id:int ):
    db_localidad = Localidad.get(db, localidad_id)
    if not db_localidad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Localidad not found')
    return db_localidad

def delete_localidad(db: Session, localidad_id:int ):

    db_localidad = Localidad.get(db, localidad_id)
    if not db_localidad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Localidad not found')
    Localidad.delete(db_localidad, db)
    
def get_localidad_by_cultivo(db: Session, cultivo_id:int ):
    db_localidad = Localidad.get_by_cultivo_id(db, cultivo_id)
    if not db_localidad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Localidad not found')
    
    return db_localidad

def get_localidades_by_user_id(db: Session, cultivo_id:int ):
    db_localidad = Localidad.get_by_user_id(db, cultivo_id)
    if not db_localidad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Localidad not found')

    return db_localidad

async def make_predictions(db:Session, local:Localidad):
    try:
        data = await get_history_date(local.latitude, local.longitude)
        predict.predict(db , data, local)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))
