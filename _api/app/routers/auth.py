# import jwt
from fastapi import Depends, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from .._view.auth import (
    is_user_autenticate,
    register as register_view,
    login as login_view,
    status as status_view
)
from .._schemas.user import RequestUserCreate
from .._schemas.token import RequestToken

from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/login", response_model=RequestToken)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
                db: Session = Depends(get_db)):
    return login_view(form_data, db)

@router.post("/register")
async def register(form_data: Annotated[RequestUserCreate, Depends()], 
                   db: Session = Depends(get_db)):
    register_view(form_data, db)

@router.get("/status")
async def status( is_autenticate: Annotated[bool, Depends(is_user_autenticate)]):
    return status_view()

# @router.post("/logout")
# async def logout(
#     current_user: models.User = Depends(oauth2_scheme), db: Session = Depends(get_db)
# ):
#     # Option 1: Revoke the access token (if your token storage supports it)
#     # crud.revoke_access_token(db, current_user.id, current_user.access_token)

#     # Option 2: Invalidate the access token (if your token storage doesn't support revocation)
#     # current_user.access_token = None  # Or set it to an invalid value
#     # db.commit()

#     return {"message": "Successfully logged out"}
