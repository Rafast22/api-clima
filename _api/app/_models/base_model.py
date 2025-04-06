
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, Column, Integer
from ..database import Base
from sqlalchemy import select, func
class BaseModel(Base):
    __abstract__ = True  
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    @classmethod
    def create(cls, session, **kwargs):
        instance = cls(**kwargs)
        session.add(instance)
        session.commit()
        session.refresh(instance)
        return instance

    @classmethod
    def get(cls, session, id):
        return session.query(cls).filter_by(id=id).first()

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()
    
    @classmethod
    def get_all_paginated(cls, session:Session, page: int = 1, per_page: int = 10):

        query = select(cls).order_by(cls.id)
        paginated_result = cls.paginate_query(session, query, page, per_page)
        return paginated_result

    @classmethod
    def paginate_query(cls, session, query, page: int = 1, per_page: int = 10):
        page = max(1, page)
        per_page = max(1, min(per_page, 100))
        count_query = select(func.count()).select_from(query.subquery())
        total_items = session.scalar(count_query)
        # total_items = query.count()
        offset = (page - 1) * per_page
        paginated_query = query.offset(offset).limit(per_page)
        items = session.scalars(paginated_query).all()

        total_pages = (total_items + per_page - 1) // per_page
        return {
            "items": items,
            "total_items": total_items,
            "total_pages": total_pages,
            "current_page": page,
            "per_page": per_page
        }
    

    def update(self, session, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key) and value is not None:
                setattr(self, key, value)
        session.commit()
        session.refresh(self)
        return self

    def delete(self, session):
        session.delete(self)
        session.commit()
