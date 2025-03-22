from fastapi import Depends, APIRouter, status, Body
from typing import Annotated, Union
from .._schemas.user import RequestUserResponse, RequestUserUpdate
from .._view.user import (
    update_user as update_user_view,
    get_user_by_id as get_user_by_id_view,
    delete_user_by_id as delete_user_by_id_view
)
from ..database import get_db
from .._view.auth.auth import is_user_autenticate
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/user", tags=["User"])

@router.put("", status_code=status.HTTP_204_NO_CONTENT)
async def update_user(is_autenticate: Annotated[bool, Depends(is_user_autenticate)], 
                      user: RequestUserUpdate = Body(...), 
                      db: Session = Depends(get_db)):
    
    return update_user_view(db, user)
    
@router.get("/{user_id}", response_model=RequestUserResponse)
async def get_user_by_id(is_autenticate: Annotated[bool, Depends(is_user_autenticate)], 
                         user_id: int, 
                         db: Session = Depends(get_db)):
    
    return get_user_by_id_view(db, user_id)

@router.delete("/{user_id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_user_by_id(is_autenticate: Annotated[bool, Depends(is_user_autenticate)], 
                            user_id: int, 
                            db: Session = Depends(get_db)):
    
    delete_user_by_id_view(db, user_id)
    
