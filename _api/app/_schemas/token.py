from pydantic import BaseModel
from typing import Union
class RequestToken(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None