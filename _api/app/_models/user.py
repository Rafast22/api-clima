from sqlalchemy import Column, Integer, String, Boolean, DateTime, or_
from sqlalchemy.sql import func
from ..database import pwd_context, Base
from .._schemas.user import RequestUserCreate, RequestUserUpdate
from sqlalchemy.orm import Session, relationship, load_only
from fastapi import HTTPException, status
from .base_model import BaseModel

class User(BaseModel):
    __tablename__ = "User"
         
    username = Column(String, index=True, unique=True)
    password = Column(String, index=True)
    full_name = Column(String, index=True)
    email = Column(String, index=True, unique=True)
    is_staff = Column(Boolean, index=True, default=False)
    is_active = Column(Boolean, index=True, default=True)
    last_login = Column(DateTime, index=True, onupdate=func.now())
    date_joined = Column(DateTime, index=True, server_default=func.now())
    role = Column(String, index=True, default="User")
    cultivos = relationship("Cultivo", backref="User", cascade="all, delete-orphan", passive_deletes=True)
    localidades = relationship("Localidad", backref="User", cascade="all, delete-orphan", passive_deletes=True)

    def verify_password(self, plain_password):
        return pwd_context.verify(plain_password, self.password)

    def get_password_hash(password):
        return pwd_context.hash(password)

    @staticmethod
    def get_user_by_email(db: Session, q: str):
        return db.query(User).options(load_only(User.id,
                                                User.username,
                                            User.email,
                                            User.full_name,
                                            User.password)).filter(User.email == q).first()
    @staticmethod
    def get_user(db:Session, email: str=None):
        if email:
            return User.get_user_by_email(db, email)
    
    @staticmethod
    def get_user_by_username(db: Session, username: str):
        return db.query(User).options(load_only(User.id,
                                                User.username,
                                            User.email,
                                            User.full_name,
                                            User.password)).filter(User.username == username).first()