
from pydantic import BaseModel

class RequestLocalidadBase(BaseModel):
    latitude: str 
    longitude: str
    user_id:int | None = None
    cultivo_id:int | None = None
        
class RequestLocalidadCreate(RequestLocalidadBase):
    pass

class RequestLocalidad(RequestLocalidadBase):
    id: int
    class Config:
        from_attributes = True

  