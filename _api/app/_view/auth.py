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
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):

    credentials_exception = HTTPException(
        status_code=httpStatus.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, str(SECRET_KEY), algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception

        token_data = TokenData(username=username)
    except InvalidTokenError as e:
        raise credentials_exception

    db_user = await user.get_user(email=token_data.email)

    if db_user is None:
        raise credentials_exception
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
    credentials_exception = HTTPException(
        status_code=httpStatus.HTTP_401_UNAUTHORIZED,
        detail="Username or Password wrng",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user_db = user.get_user_by_email_or_username(db,username)
    try:
        if not user_db:
            return {'reponse':False, 'error':'User not Found'}
        if not user_db.verify_password(password):
            return {'reponse':False, 'error':'Incorrect Password'}
            
        return user_db
    except UnknownHashError:
      raise credentials_exception
   
async def is_user_autenticate(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=httpStatus.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    return True

async def get_current_user(db: Session, token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=httpStatus.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    db_user = user.get_user_by_username(db, username=token_data.username)
    if db_user is None:
        raise credentials_exception
    return db_user

def register(request_user:RequestUserCreate, db: Session) -> RequestUser:
    user_db = user.get_user(db, username=request_user.username)
    if user_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    else:
        user_db = user.get_user(db, email=request_user.email)
        if user_db:
            raise HTTPException(status_code=400, detail="Email already registered")
    return user.create_user(db, request_user)

def login(form_data: OAuth2PasswordRequestForm, db: Session) -> RequestToken:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=httpStatus.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    response = RequestToken(access_token=access_token, token_type="bearer")
    return response

def logout(current_user:User = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    pass

def status():
    return {"logged": True}
    