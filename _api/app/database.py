from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi.security import OAuth2PasswordBearer, OAuth2AuthorizationCodeBearer
from passlib.context import CryptContext
import time
import os
import sys



gettrace = getattr(sys, 'gettrace', None)

IS_DOCKER = os.getenv('IS_DOCKER')

SQLITE_URL = "sqlite:///./sql_app.db"
DATABASE_URL = os.getenv('DATABASE_URL')
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = os.getenv('SMTP_PORT')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
GOOGLE_REDIRECT_URI_HML = os.getenv('GOOGLE_REDIRECT_URI_HML')
SECRET_KEY = os.getenv('SECRET_KEY')
print(DATABASE_URL)
print(SENDER_EMAIL)
print(SMTP_PASSWORD)
print(SMTP_SERVER)
print(SMTP_PORT)
print(ALGORITHM)
print(ACCESS_TOKEN_EXPIRE_MINUTES)
print(GOOGLE_CLIENT_ID)
print(GOOGLE_CLIENT_SECRET)
print(GOOGLE_REDIRECT_URI_HML)
print(SECRET_KEY)

if not IS_DOCKER:
    if not DATABASE_URL:
        DATABASE_URL = SQLITE_URL
    else:
        DATABASE_URL = 'postgresql://postgres:Rei12Rom%40@localhost:5432/DB'
    if gettrace():
        SECRET_KEY = 'test'
        ACCESS_TOKEN_EXPIRE_MINUTES = 1000
        ALGORITHM = 'HS256'
        engine = create_engine(DATABASE_URL)
    elif DATABASE_URL == SQLITE_URL:
        engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
        SECRET_KEY = "test"
        ACCESS_TOKEN_EXPIRE_MINUTES = 1000
        ALGORITHM = 'HS256'
else:
    print(IS_DOCKER)
    time.sleep(5)
    engine = create_engine(DATABASE_URL)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")
oauth2_scheme_google = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://accounts.google.com/o/oauth2/auth",
    tokenUrl="https://oauth2.googleapis.com/token",
    scopes={'openid':'openid', 'profile':'profile','email':'email'}
)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
async def create_databases():
    Base.metadata.create_all(bind=engine)
    