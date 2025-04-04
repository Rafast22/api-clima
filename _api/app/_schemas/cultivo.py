
from pydantic import BaseModel


class RequestCultivoBase(BaseModel):
    name: str
    variety: str 
    cycle_duration: int
        
class RequestCultivoCreate(RequestCultivoBase):
    pass

class RequestCultivo(RequestCultivoBase):
    id: int
    class Config:
        from_attributes = True

  