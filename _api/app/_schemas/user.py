from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Union
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
    email: Union[EmailStr, None] = None
    is_staff: Union[bool, None] = False
    is_active: Union[bool, None] = True
    role: Union[str, None] = "user"
    

class RequestUserCreate(RequestUserBase):
    class Config:
        from_attributes = True

class RequestUserUpdate(RequestUserBase):
    id: int 
    class Config:
            from_attributes = True

class RequestUserResponse(RequestUserUpdate):
    cultivos:list[RequestCultivo] = []

    

    