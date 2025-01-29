from fastapi import Depends, APIRouter, status
from typing import Annotated, List
from .._schemas.cultivo import RequestCultivo, RequestCultivoCreate
from .._view.cultivo import (
    update_cultivo as update_cultivo_view,
    get_cultivo_by_id as get_cultivo_by_id_view, 
    delete_cultivo_by_id as delete_cultivo_by_id_view, 
    get_cultivos_by_user_id as get_cultivos_by_user_id_view, 
    create_cultivo as create_cultivo_view
)
from ..database import get_db
from .._view.auth import is_user_autenticate
from sqlalchemy.orm import Session


router = APIRouter(prefix="/api/user/cultivo", tags=["Cultivo"])
    
@router.get("/{cultivo_id}", response_model=RequestCultivo)
async def get_cultivo_by_id(cultivo_id: int, 
                            is_autenticate: Annotated[bool, Depends(is_user_autenticate)], 
                            db: Session = Depends(get_db)
                            ):
    return get_cultivo_by_id_view(db, cultivo_id)

@router.get("/{user_id}", response_model=List[RequestCultivo])
async def get_cultivos_by_user_id(user_id: int, 
                                  is_autenticate: Annotated[bool, Depends(is_user_autenticate)], 
                                  db: Session = Depends(get_db)
                                  ):
    return get_cultivos_by_user_id_view(db, user_id)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_cultivo(cultivo: Annotated[RequestCultivoCreate, Depends()], 
                         is_autenticate: Annotated[bool, Depends(is_user_autenticate)], 
                         db: Session = Depends(get_db)
                         ):
    create_cultivo_view(db, cultivo)

@router.put("/{cultivo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_cultivo(user: Annotated[RequestCultivo, Depends()], 
                         is_autenticate: Annotated[bool, Depends(is_user_autenticate)], 
                         db: Session = Depends(get_db)
                         ):
    return update_cultivo_view(db, user)

@router.delete("/{cultivo_id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_cultivo_by_id(cultivo_id: int, 
                               is_autenticate: Annotated[bool, Depends(is_user_autenticate)], 
                               db: Session = Depends(get_db)
                               ):
    delete_cultivo_by_id_view(db, cultivo_id)