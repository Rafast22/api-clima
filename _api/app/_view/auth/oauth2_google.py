import aiohttp
from ..._schemas.token import TokenData, RequestToken
from fastapi import HTTPException
from fastapi import Depends, status
from fastapi.responses import RedirectResponse
from aiohttp import ClientSession
from typing import Annotated, Union
from datetime import timedelta, timezone, datetime
from ...database import (
    SECRET_KEY, 
    ALGORITHM, 
    ACCESS_TOKEN_EXPIRE_MINUTES, 
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    GOOGLE_REDIRECT_URI_HML,
    get_db, 
    oauth2_scheme,
    oauth2_scheme_google)
import jwt
from jwt import InvalidTokenError

async def post_data(session: ClientSession, url, data):
    async with session.post(url, data=data) as response:
        return  response.status, await response.json()

async def get_data(session: ClientSession, url, headers):
    async with session.get(url, headers=headers) as response:
        return  response.status, await response.json()

async def fetch_request(url, data):
    async with ClientSession() as session:
        status, response = await post_data(session, url, data)
    return status, response


async def auth_google_callback(code: str):
        async with ClientSession() as session:
            status_code, token_response = await post_data(session,
                                               'https://oauth2.googleapis.com/token', 
                                               data={
                                                "code": code,
                                                "client_id": GOOGLE_CLIENT_ID,
                                                "client_secret": GOOGLE_CLIENT_SECRET,
                                                "redirect_uri": GOOGLE_REDIRECT_URI_HML,
                                                "grant_type": "authorization_code",
                                                'access_type':'offline'
                                                })
            
        if status_code != 200:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao obter token")
        access_token = create_access_token(data={"sub": token_response}, expires_delta=timedelta(seconds=token_response['expires_in']))
        return RequestToken(access_token=access_token, token_type="bearer")
        # return RequestToken(**token_response)

async def get_userinfo(token: str = Depends(oauth2_scheme_google)):
    async with ClientSession() as session:
        status_code, userinfo_response = await get_data(session,
                                                     "https://www.googleapis.com/oauth2/v1/userinfo",
                                                     headers={"Authorization": f"Bearer {token}"})
        userinfo_data = userinfo_response
        if status_code != 200:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao obter informações do usuário")
        return userinfo_data


async def verify_google_token(token: str):
    async with ClientSession() as session:
        status_code, response = await get_data(session,
                                                    f"https://oauth2.googleapis.com/tokeninfo?access_token={token}",
                                                    # f"https://oauth2.googleapis.com/tokeninfo?id_token={token}",
                                                    None)
        
        if status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token do Google inválido",
            )
        return response
    
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt