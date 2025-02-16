# import jwt
from fastapi import Depends, status, APIRouter, Body
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from .._view.auth.auth import (
    is_user_autenticate,
    register as register_view,
    login as login_view)
from .._view.auth.oauth2_google import (
        auth_google_callback as auth_google_callback_view,
        get_userinfo as get_userinfo_view,
)
from .._schemas.user import RequestUserCreate
from .._schemas.token import RequestToken

from sqlalchemy.orm import Session
from ..database import get_db, oauth2_scheme_google

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/login", response_model=RequestToken)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
                db: Session = Depends(get_db)):
    return login_view(form_data, db)

@router.post("/register")
async def register(form_data: RequestUserCreate = Body(...), 
                   db: Session = Depends(get_db)):
    register_view(form_data, db)

@router.get("/google/callback")
async def auth_google_callback(code: str):
    return await auth_google_callback_view(code)

@router.get("/userinfo")
async def get_userinfo(token: str = Depends(oauth2_scheme_google)):
    # async with httpx.AsyncClient() as client:
    #     userinfo_response = await client.get(
    #         "https://www.googleapis.com/oauth2/v1/userinfo",
    #         headers={"Authorization": f"Bearer {token}"},
    #     )
    #     userinfo_data = userinfo_response.json()
    #     if userinfo_response.status_code != 200:
    #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao obter informações do usuário")
    #     return userinfo_data
    return await get_userinfo_view(token)
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
