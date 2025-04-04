
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer
from ..database import Base
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
