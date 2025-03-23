from fastapi import Depends, APIRouter, Query
from typing import Union, Annotated, List
from .._schemas.user import RequestUserCreate
from .._models.predictions import Predictions
from .._view.previcion import (get_previcion_by_day as get_previcion_by_day_view, 
                               get_previcion_semana as get_previcion_semana_view,
                               get_previcion_semana_by_data as get_previcion_semana_by_data_view,
                               get_previcion_periodo as get_previcion_periodo_view,
                               get_previcion_total_from_today as get_previcion_total_from_today_view
                            ) 
from ..database import get_db
from .._view.auth.auth import is_user_autenticate
from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta

from .._view.localidad import localidad as M
from ..interceptor.nasa_request import get_history_date
from ..interceptor.predict import predict
router = APIRouter(prefix="/api/user/weather/forecast", tags=["Previciones"])


@router.get("/week",
             summary="Get weekend predict list", 
             description="Returns a list of weather forecasts for a week")
async def get_previcion_semana(is_autenticate: Annotated[bool, Depends(is_user_autenticate)],
                               localidad:int, db: Session = Depends(get_db)):
    return get_previcion_semana_view(db, localidad)

@router.post("/week/date",
             summary="Get weekend predict list by date range", 
             description="Returns a list of weather forecasts for a week")
async def get_previcion_semana_by_date(is_autenticate: Annotated[bool, Depends(is_user_autenticate)],
                               localidad:int, data_inicial:datetime, data_final:datetime,
                               db: Session = Depends(get_db), ):
    return get_previcion_semana_by_data_view(db, localidad, data_inicial, data_final)

@router.post("/range", 
             summary="Get predict list by date range", 
             description="Returns a list of weather forecasts for a date range")

async def get_previcion_periodo(is_autenticate: Annotated[bool, Depends(is_user_autenticate)],
                                tipo:int, cultivo:int, localidad:int,
                                fecha_inicio: datetime = Query(..., description="Start date of the period in YYYY-MM-DD format."),
                                fecha_fin: datetime = Query(..., description="End date of the period in YYYY-MM-DD format."), 
                                db: Session = Depends(get_db) ):

    return get_previcion_periodo_view(db, fecha_inicio, fecha_fin, tipo, cultivo, localidad)

@router.post("/day", 
             summary="Get predict list by day", 
             description="Returns a list of weather forecasts for a date range")

async def get_previcion_periodo_day(is_autenticate: Annotated[bool, Depends(is_user_autenticate)],
                                day: datetime = Query(..., description="Start date of the period in YYYY-MM-DD format."),
                                db: Session = Depends(get_db) ):

    return get_previcion_by_day_view(db, day)

@router.post("", 
             summary="Get predict list", 
             description="Returns a list of weather forecasts for a date range")

async def get_previcion_periodo_month(is_autenticate: Annotated[bool, Depends(is_user_autenticate)],
                                      tipo:int, cultivo:int, localidad:int,
                                      db: Session = Depends(get_db) ):

    return get_previcion_total_from_today_view(db, tipo, cultivo, localidad)


@router.get("testP")
async def p(db: Session = Depends(get_db)):
    d = db

    l = M.get_by_latitude_longitude(d, "-25.65", "-54.70")
    if not l:
        new = M.RequestLocalidadCreate(**{'latitude':'-25.65', 'longitude':'-54.70', 'user_id':None, 'cultivo_id':None} )
        l = M.create(d, new)
    
    h = await get_history_date(l.latitude, l.longitude)
    predict(d, h, l)
    del h, l, d