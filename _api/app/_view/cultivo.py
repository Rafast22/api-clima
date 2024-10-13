import jwt
from typing import  Annotated
from jwt.exceptions import InvalidTokenError
from ..database import SECRET_KEY, ALGORITHM
from .._models.cultivo import Cultivo
from ..database import oauth2_scheme
from .._models import cultivo
from .._schemas.cultivo import RequestCultivo, RequestCultivoCreate
from .._schemas.token import RequestToken, TokenData
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends


def update(db: Session, u: RequestCultivo) -> RequestCultivo:
    credentials_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Cultivo not found",
        headers={"WWW-Authenticate": "Bearer"},
    )    
   
    db_cultivo = cultivo.get_cultivo_by_id(db, u.id)
    if db_cultivo is None:
        raise credentials_exception
        
    db_cultivo = cultivo.update_cultivo(db, u)

    return db_cultivo

    # if not db_cultivo:
    #     raise HTTPException(status_code=404, detail="Usuário não encontrado")
    # return db_cultivo

def get_by_id(db: Session, cultivo_id:int ) -> RequestCultivo:
    db_cultivo = cultivo.get_cultivo_by_id(db, cultivo_id)
    if not db_cultivo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_cultivo

def delete_cultivo(db: Session, cultivo_id:int ):
    try:
        cultivo.delete_cultivo(db, cultivo_id)
        return {"ok": True}
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
        
def get_by_user_id(db: Session, user_id:int ) -> RequestCultivo:
    db_cultivo = cultivo.get_cultivos_usuario(db, user_id)
    if not db_cultivo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_cultivo

def create(db: Session, u: RequestCultivoCreate) -> RequestCultivo:
    db_cultivo = cultivo.create_cultivo(db, u.id)

    return db_cultivo

    # if not db_cultivo:
    #     raise HTTPException(status_code=404, detail="Usuário não encontrado")
    # return db_cultivo

