# import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from jwt.exceptions import InvalidTokenError
# from passlib.context import CryptContext
from pydantic import BaseModel
from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, status
from .._view import auth
from .._view.auth import is_user_autenticate
from .._schemas.user import RequestUserCreate
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter()


@router.post("/api/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    return auth.login(form_data, db)

@router.post("/api/register")
async def register(form_data: RequestUserCreate, db: Session = Depends(get_db)):
    return auth.register(form_data, db)

@router.get("/api/status")
async def status( is_autenticate: Annotated[bool, Depends(is_user_autenticate)]):
    return auth.status()

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
