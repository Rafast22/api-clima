from fastapi import Depends, APIRouter, Query
from typing import Union, Annotated, List
from .._schemas.user import RequestUserCreate
from .._models.predictions import Predictions
from .._view.previcion import (get_previcion_by_day as get_previcion_by_day_view, 
                               get_previcion_semana as get_previcion_semana_view,
                               get_previcion_periodo as get_previcion_periodo_view,
                            ) 
from ..database import get_db
from .._view.auth import is_user_autenticate
from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta

router = APIRouter(prefix="/api/user/weather/forecast", tags=["Previciones"])


@router.post("/week",
             summary="Get weekend predict list", 
             description="Returns a list of weather forecasts for a week")
async def get_previcion_semana(is_autenticate: Annotated[bool, Depends(is_user_autenticate)],
                               localidad:int, dia:datetime,
                               db: Session = Depends(get_db), ):
    return get_previcion_semana_view(db, localidad, dia)

@router.post("/range", 
             summary="Get predict list by date range", 
             description="Returns a list of weather forecasts for a date range")

async def get_previcion_periodo(is_autenticate: Annotated[bool, Depends(is_user_autenticate)],
                                tipo:int, cultivo:int, localidad:int,
                                fecha_inicio: datetime = Query(..., description="Start date of the period in YYYY-MM-DD format."),
                                fecha_fin: datetime = Query(..., description="End date of the period in YYYY-MM-DD format."), 
                                db: Session = Depends(get_db) ):

    return get_previcion_periodo_view(db, fecha_inicio, fecha_fin, tipo, cultivo, localidad)

