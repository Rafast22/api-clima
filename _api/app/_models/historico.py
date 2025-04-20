from sqlalchemy import Column, Integer, String, Boolean, DateTime, or_, ForeignKey, DECIMAL
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, Session
from sqlalchemy.ext.declarative import declarative_base
from ..database import Base
from .._schemas.nasa_data import RequestDataCreate, RequestData
from fastapi import HTTPException, status
from sqlalchemy import func, select
from .base_model import BaseModel
from ._base_prediction import BasePrediction
class History(BasePrediction):
    __tablename__ = "History"


    @classmethod
    def create_bulk(cls, session, data_list):
        instances = [cls(**kwargs) for kwargs in data_list]
        session.add_all(instances)
        session.commit()
    
    @classmethod
    def get_all_by_user_paginated(cls, session:Session, user_id:int, page: int = 1, per_page: int = 10):
        query = select(cls).where(cls.user_id==user_id).order_by(cls.id)
        paginated_result = cls.paginate_query(session, query, page, per_page)
        return paginated_result