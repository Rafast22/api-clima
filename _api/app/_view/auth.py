from .._models.user import User
from .._schemas.user import RequestUserCreate, RequestUser
from .._models import user
from sqlalchemy.orm import Session
from .._schemas.token import RequestToken, TokenData
from fastapi import HTTPException, status as httpStatus, Depends
from datetime import datetime, timedelta, timezone
from typing import Annotated, Union
import jwt
from passlib.exc import UnknownHashError
from ..database import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, get_db, oauth2_scheme
from jwt.exceptions import InvalidTokenError
from fastapi.security import OAuth2PasswordRequestForm

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):

    try:
        payload = jwt.decode(token, str(SECRET_KEY), algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise HTTPException(status_code=httpStatus.HTTP_404_NOT_FOUND)
        token_data = TokenData(username=username)
        db_user = await user.get_user(email=token_data.email)

    except InvalidTokenError as e:
        raise HTTPException(status_code=httpStatus.HTTP_401_UNAUTHORIZED)
    except Exception as ex:
        raise HTTPException(status_code=httpStatus.HTTP_500_INTERNAL_SERVER_ERROR)

    if db_user is None:
        raise HTTPException(status_code=httpStatus.HTTP_404_NOT_FOUND)
    
    return user

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(db: Session, username: str, password: str):
    try:
        if '@' in username:
            user_db = user.get_user_by_email(db,username)
        elif username:
            user_db = user.get_user_by_username(db,username)
        else:
            raise HTTPException(status_code=httpStatus.HTTP_400_BAD_REQUEST)
        
        if not user_db:
            raise HTTPException(status_code=httpStatus.HTTP_404_NOT_FOUND)
        if not user_db.verify_password(password):
            raise HTTPException(status_code=httpStatus.HTTP_401_UNAUTHORIZED)
        return user_db
    except UnknownHashError:
      raise HTTPException(status_code=httpStatus.HTTP_500_INTERNAL_SERVER_ERROR)
   
async def is_user_autenticate(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise HTTPException(status_code=httpStatus.HTTP_401_UNAUTHORIZED)

    except InvalidTokenError:
        raise HTTPException(status_code=httpStatus.HTTP_401_UNAUTHORIZED)
    return True

async def get_current_user(db: Session, token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=httpStatus.HTTP_401_UNAUTHORIZED)
        token_data = TokenData(username=username)
        db_user = user.get_user_by_username(db, username=token_data.username)

    except InvalidTokenError:
        raise HTTPException(status_code=httpStatus.HTTP_401_UNAUTHORIZED)
    
    if not db_user:
        raise HTTPException(status_code=httpStatus.HTTP_404_NOT_FOUND)

    return db_user

def register(request_user:RequestUserCreate, db: Session):
    try:
        user_db = user.get_user(db, username=request_user.username)
        if user_db:
            raise HTTPException(status_code=httpStatus.HTTP_400_BAD_REQUEST, detail="Username already registered")
        else:
            user_db = user.get_user(db, email=request_user.email)
            if user_db:
                raise HTTPException(status_code=httpStatus.HTTP_400_BAD_REQUEST, detail="Email already registered")
        user.create(db, request_user)
    except:
        raise HTTPException(status_code=httpStatus.HTTP_500_INTERNAL_SERVER_ERROR)


def login(form_data: OAuth2PasswordRequestForm, db: Session) -> RequestToken:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user is User:
        raise HTTPException(status_code=httpStatus.HTTP_401_UNAUTHORIZED)
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return RequestToken(access_token=access_token, token_type="bearer")

def logout(current_user:User = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    pass

def status():
    return {"logged": True}
    