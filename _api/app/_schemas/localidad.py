
from pydantic import BaseModel

class RequestLocalidadBase(BaseModel):
    latitude: str 
    longitude: str
        
class RequestLocalidadCreate(RequestLocalidadBase):
    pass

class RequestLocalidadUpdate(RequestLocalidadBase):
    class Config:
        from_attributes = True

class RequestLocalidad(RequestLocalidadBase):
    id: int
    class Config:
        from_attributes = True

  