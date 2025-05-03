from fastapi import Depends, APIRouter, HTTPException, status
from typing import Union, Annotated
from .._schemas.paginated import PaginationResponse
from .._models.user import User
from .._view import historico
from ..database import get_db
from .._view.auth.auth import is_user_autenticate, get_current_user
from sqlalchemy.orm import Session
router = APIRouter()

@router.get("/api/historico")
async def get_historico_by_usuario(is_autenticate: Annotated[bool, Depends(is_user_autenticate)], 
                                    page: int = 1, per_page: int = 10,
                                    user: User = Depends(get_current_user),
                                    db: Session = Depends(get_db)):
    return historico.get_historico_by_usuario(db, user, page, per_page)

# @router.post("/api/historico")
# async def get_historico_by_usuario_day(tipo:int, cultivo:int, dia:str, is_autenticate: Annotated[bool, Depends(is_user_autenticate)], db: Session = Depends(get_db), ):
#     return historico.get_historico_by_usuario_day(db, dia, cultivo, tipo)

