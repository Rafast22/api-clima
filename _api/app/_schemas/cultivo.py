
from pydantic import BaseModel


class RequestCultivoBase(BaseModel):
    name: str
    variety: str 
    cycle_duration: int
        
class RequestCultivoCreate(RequestCultivoBase):
    pass

class RequestCultivoUpdate(RequestCultivoBase):
    class Config:
        from_attributes = True

class RequestCultivo(RequestCultivoBase):
    class Config:
        from_attributes = True

  