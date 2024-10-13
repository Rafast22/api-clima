from .._models import localidad, nasa_data
from .._schemas.localicad import RequestLocalidad, RequestLocalidadCreate
from .._schemas.nasa_data import RequestDataCreate
from sqlalchemy.orm import Session
from ..interceptor.nasa_request import get_history_date
from fastapi import HTTPException, status, Depends

async def update(db: Session, u: RequestLocalidad) -> RequestLocalidad:
    credentials_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Cultivo not found",
        headers={"WWW-Authenticate": "Bearer"},
    )    
   
    db_localidad = localidad.get_by_id(db, u.id)
    if db_localidad is None:
        raise credentials_exception
        
    db_localidad = localidad.update(db, u)

    return db_localidad

    # if not db_localidad:
    #     raise HTTPException(status_code=404, detail="Usuário não encontrado")
    # return db_localidad

async def get_by_id(db: Session, localidad_id:int ) -> RequestLocalidad:
    db_localidad = localidad.get_by_id(db, localidad_id)
    if not db_localidad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Localidad not found")
    return db_localidad

async def delete(db: Session, localidad_id:int ):
    try:
        localidad.delete(db, localidad_id)
        return {"ok": True}
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
        
async def get_by_cultivo_id(db: Session, cultivo_id:int ) -> RequestLocalidad:
    db_localidad = localidad.get_by_cultivo_id(db, cultivo_id)
    if not db_localidad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Localidad not found")
    return db_localidad

async def get_by_user_id(db: Session, cultivo_id:int ) -> RequestLocalidad:
    db_localidad = localidad.get_by_user_id(db, cultivo_id)
    if not db_localidad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Localidad not found")
    return db_localidad

async def create(db: Session, u: RequestLocalidadCreate) -> RequestLocalidad:
    history_data:list[RequestDataCreate] = await get_history_date(u.latitude, u.longitude)
    db_localidad = localidad.create(db, u)
    nasa_data.create_bulk(db, history_data,db_localidad.id)
    return db_localidad
