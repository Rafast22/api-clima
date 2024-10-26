import jwt
from typing import  Annotated, List
from jwt.exceptions import InvalidTokenError
from ..database import SECRET_KEY, ALGORITHM
from .._models.nasa_data import History_Data
from ..database import oauth2_scheme
from .._models import nasa_data
from .._schemas.nasa_data import RequestData
from .._schemas.token import RequestToken, TokenData
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends

def get_historico_by_usuario(db: Session, user_id:int) -> List[History_Data]:
    db_nasa_data = nasa_data.get_historico_by_usuario(db, user_id)
    if not db_nasa_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_nasa_data
