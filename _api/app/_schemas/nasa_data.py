
from pydantic import BaseModel
from typing import Union, Optional
from datetime import datetime

class RequestDataBase(BaseModel):
    date: datetime | None = None
    prectotcorr: float | None = None
    rh2m: float | None = None
    qv2m: float | None = None
    t2m: float | None = None
    ws2m: float | None = None
    accuracy: float | None = None
    probability_rain: float | None = None
    planting: int | None = None
    harvest: int | None = None
    localidad_id: int
    user_id: int | None = None
    
        
class RequestDataCreate(RequestDataBase):
    class Config:
        from_attributes = True

class RequestData(RequestDataBase):
    id: int
    class Config:
        from_attributes = True

