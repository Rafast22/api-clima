
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
        
class RequestDataCreate(RequestDataBase):
    class Config:
        from_attributes = True

class RequestData(RequestDataBase):
    id: int
    class Config:
        from_attributes = True

