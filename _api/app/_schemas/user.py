from sqlalchemy import Column, Integer, String, Boolean, DateTime, or_
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, EmailStr, Field
from typing import Union
from sqlalchemy.orm import Session
from .._schemas.cultivo import RequestCultivo

      
# class ItemBase(BaseModel):
#     title: str
#     description: Union[str, None] = None


# class ItemCreate(ItemBase):
#     pass


# class Item(ItemBase):
#     id: int
#     owner_id: int

#     class Config:
#         orm_mode = True


# class UserBase(BaseModel):
#     email: str


# class UserCreate(UserBase):
#     password: str


# class User(UserBase):
#     id: int
#     is_active: bool
#     items: list[Item] = []

#     class Config:
#         orm_mode = True

class RequestUserBase(BaseModel):
    username: str
    password: str
    full_name: str
    email: Union[EmailStr, None] = Field(default=None)
    is_staff: Union[bool, None] = False
    is_active: Union[bool, None] = True
    role: Union[str, None] = "user"
    class Config:
        from_attributes = True

class RequestUserCreate(RequestUserBase):
    pass

class RequestUser(RequestUserBase):
    id: int 
    last_login: datetime
    date_joined: datetime
    cultivos:list[RequestCultivo] = []
    

    