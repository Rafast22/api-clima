from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import os
import sys
gettrace = getattr(sys, 'gettrace', None)

SQLITE_URL = "sqlite:///./sql_app.db"
DATABASE_URL = os.getenv('DATABASE_URL')
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = os.getenv('SMTP_PORT')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
IS_DOCKER = os.getenv('IS_DOCKER')

# DATABASE_URL = POSTGRESQL_URL
# DATABASE_URL = SQLITE_URL
# DATABASE_URL = 'postgresql://postgres:Rei12Rom%40@localhost:5432/DB'

if not IS_DOCKER:
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
        SECRET_KEY = os.getenv('SECRET_KEY')
        engine = create_engine(DATABASE_URL)



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
async def create_database():
    Base.metadata.create_all(bind=engine)
    