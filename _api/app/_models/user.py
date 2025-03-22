from sqlalchemy import Column, Integer, String, Boolean, DateTime, or_
from sqlalchemy.sql import func
from ..database import pwd_context, Base
from .._schemas.user import RequestUserCreate, RequestUserUpdate
from sqlalchemy.orm import Session, relationship, load_only
from fastapi import HTTPException, status


class User(Base):
    __tablename__ = "User"
    def __init__(self, user:RequestUserCreate | RequestUserUpdate, user_id:int=None):
        self.username = user.username 
        if user.password:
            self.password = pwd_context.hash(user.password)
        self.full_name = user.full_name  
        self.email = user.email  
        self.is_staff = user.is_staff  
        self.is_active = user.is_active  
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
    cultivos = relationship("Cultivo", backref="User", cascade="all, delete-orphan", passive_deletes=True)
    localidades = relationship("Localidad", backref="User", cascade="all, delete-orphan", passive_deletes=True)
    
    

    def verify_password(self, plain_password):
        return pwd_context.verify(plain_password, self.password)


    def get_password_hash(password):
        return pwd_context.hash(password)
    
    # @property
    # def passwrd(self):
    #     return self._pass
    # @passwrd.setter
    # def passwrd(self, value):
    #     self._pass = value
def get_by_id(db: Session, user_id: int):
    return db.get(User, user_id)

def get_user_by_email(db: Session, q: str):
    return db.query(User).options(load_only(User.id,
                                            User.username,
                                            User.email,
                                            User.full_name,
                                            User.password)).filter(User.email == q).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).options(load_only(User.id,
                                            User.username,
                                            User.email,
                                            User.full_name,
                                            User.password)).filter(User.username == username).first()

def get_user( db:Session, email: str=None):
    if email:
        return get_user_by_email(db, email)

def create(db: Session, user: RequestUserCreate):
    db_user = User(user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    

def update(db: Session, user: RequestUserUpdate):
    db_user = db.query(User).filter(User.id == user.id).first()
    if db_user is None:
        raise None
    for key, value in vars(user).items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user

def delete(db: Session, user_id: int):
    db_user = db.get(User, user_id)
    db.delete(db_user)
    db.commit()

