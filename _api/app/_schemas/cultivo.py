
from pydantic import BaseModel
from typing import Union, Optional


class RequestCultivoBase(BaseModel):
    # create_date:Union[None] = None
    # update_date:Union[None] = None
    # user:Union[None] = None
    name: str
    variety: str 
    cycle_duration: int
    user_id:int
        
class RequestCultivoCreate(RequestCultivoBase):
    pass

class RequestCultivo(RequestCultivoBase):
    id: int
    class Config:
        from_attributes = True

  