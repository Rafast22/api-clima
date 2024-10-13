from sqlalchemy import Column, Integer, String, Boolean, DateTime, or_
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import Union
from ..database import pwd_context, Base
from .._schemas.user import RequestUserCreate, RequestUser
from sqlalchemy.orm import Session, Query
from fastapi import HTTPException, status
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "User"
    def __init__(self, user:RequestUser, user_id:int=None):
        # if user_id:
        #     self.id = user_id
        self.username = user.username 
        if user.password:
            self.password = pwd_context.hash(user.password)
        self.full_name = user.full_name  
        self.email = user.email  
        self.is_staff = user.is_staff  
        self.is_active = user.is_active  
        # self.last_login = user.last_login  
        # self.date_joined = user.date_joined  
        self.role = user.role  
         
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, unique=True)
    password = Column(String, index=True)
    full_name = Column(String, index=True)
    email = Column(String, index=True, unique=True)
    is_staff = Column(Boolean, index=True, default=False)
    is_active = Column(Boolean, index=True, default=True)
    last_login = Column(DateTime, index=True, onupdate=func.now())
    date_joined = Column(DateTime, index=True, server_default=func.now())
    role = Column(String, index=True, default="User")
    # cultivos = relationship("Cultivos", back_populates="user", cascade="all, delete-orphan")
    
    

    def verify_password(self, plain_password):
        return pwd_context.verify(plain_password, self.password)


    def get_password_hash(password):
        return pwd_context.hash(password)




def get_user_by_id(db: Session, user_id: int):
    return db.get(User, user_id)

def get_user_by_email_or_username(db: Session, q: str):
    return db.query(User).filter(or_(User.email == q, User.username == q)).first()

def get_user_by_email(db: Session, q: str):
    return db.query(User).filter(User.email == q).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user( db:Session, email: str=None, username: str = None):
    if email:
        return get_user_by_email(db, email)
    elif username:
        return get_user_by_username(db, username)

def create_user(db: Session, user: RequestUserCreate):
    db_user = User(user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user: RequestUser):
    db_user = db.query(User).filter(User.id == user.id).first()
    if db_user is None:
        raise None

    for key, value in vars(user).items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(db_user)
    db.commit()

