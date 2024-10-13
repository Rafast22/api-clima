
from pydantic import BaseModel
from typing import Union, Optional


class RequestLocalidadBase(BaseModel):
    # create_date:Union[None] = None
    # update_date:Union[None] = None
    # user:Union[None] = None
    latitude: str 
    longitude: str
    user_id:int
    cultivo_id:int | None = None
        
class RequestLocalidadCreate(RequestLocalidadBase):
    pass

class RequestLocalidad(RequestLocalidadBase):
    id: int
    class Config:
        from_attributes = True

  