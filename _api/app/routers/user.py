from fastapi import Depends, APIRouter, status, Body, HTTPException
from typing import Annotated
from .._schemas.user import RequestUserResponse, RequestUserUpdate
from .._view.user import (
    update_user as update_user_view,
    get_user_by_id as get_user_by_id_view,
    delete_user_by_id as delete_user_by_id_view
)
from .._models.user import User
from ..database import get_db
from .._view.auth.auth import is_user_autenticate, get_current_user
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/user", tags=["User"])

@router.put("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_user(is_autenticate: Annotated[bool, Depends(is_user_autenticate)], 
                      user_id:int,
                      user: RequestUserUpdate = Body(...), 
                      db: Session = Depends(get_db)):
    
    return update_user_view(db, user_id, user)

@router.post("", status_code=status.HTTP_204_NO_CONTENT)
async def create_user(is_autenticate: Annotated[bool, Depends(is_user_autenticate)], 
                      user: RequestUserUpdate = Body(...), 
                      db: Session = Depends(get_db),
                      me: User = Depends(get_current_user)):
    if(me.role == 'user'): 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Logged-in user does not have permission to use this route.")
    return update_user_view(db, user)

@router.get("/{user_id}", response_model=RequestUserResponse)
async def get_by_id(is_autenticate: Annotated[bool, Depends(is_user_autenticate)], 
                    user_id: int, 
                    db: Session = Depends(get_db)):
    return get_user_by_id_view(db, user_id)

@router.delete("/{user_id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_user_by_id(is_autenticate: Annotated[bool, Depends(is_user_autenticate)], 
                            user_id: int, 
                            me: User = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    if(me.id != user_id): 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Logged-in user does not have permission to use this route.")

    delete_user_by_id_view(db, user_id)

@router.get("/me", status_code=status.HTTP_200_OK)
async def get_me(is_autenticate: Annotated[bool, Depends(is_user_autenticate)], 
                            db: Session = Depends(get_db),
                            me: User = Depends(get_current_user)):
    return me
    
