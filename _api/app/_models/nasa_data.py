from sqlalchemy import Column, Integer, String, Boolean, DateTime, or_, ForeignKey, DECIMAL
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, Session
from sqlalchemy.ext.declarative import declarative_base
from ..database import Base
from .._schemas.nasa_data import RequestDataCreate, RequestData
from fastapi import HTTPException, status

class History_Data(Base):
    __tablename__ = "History_Data"

    def __init__(self, history: RequestDataCreate):
        self.date = history.date
        self.prectotcorr = history.prectotcorr
        self.rh2m = history.rh2m
        self.qv2m = history.qv2m
        self.t2m = history.t2m
        self.ws2m = history.ws2m

    # user = relationship("User", back_populates="Data") 
    # cultivo = relationship("Cultivos", back_populates="Data") 
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, nullable=True)
    prectotcorr = Column(DECIMAL(10, 3), nullable=True)
    rh2m = Column(DECIMAL(10, 3), nullable=True)
    qv2m = Column(DECIMAL(10, 3), nullable=True)
    t2m = Column(DECIMAL(10, 3), nullable=True)
    ws2m = Column(DECIMAL(10, 3), nullable=True)
    localidad_id = Column(Integer, ForeignKey('Localidad.id'), nullable=False)
    

def get_by_id(db: Session, Data_id: int):
    return db.get(History_Data, Data_id)

def create(db: Session, Data: RequestDataCreate):
    db_history = History_Data(Data)
    db.add(db_history)
    db.commit()
    db.refresh(db_history)
    return db_history

def update(db: Session, Data: RequestData):
    db_history = db.get(History_Data, Data.id)
    if db_history is None:
        raise None

    for key, value in vars(Data).items():
        setattr(db_history, key, value)

    db.commit()
    db.refresh(db_history)
    return db_history

def delete(db: Session, user_id: int):
    db_history = db.get(History_Data, user_id)
    if not db_history:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="History_Data not found")
    db.delete(db_history)
    db.commit()

def gravar_bulk(db: Session, data: list[RequestDataCreate]):
    
    """
    Grava múltiplos registros em uma tabela de forma eficiente.

    Args:
        db: Sessão SQLAlchemy.
        data: Lista de objetos a serem inseridos.
    """
    db.bulk_save_objects(data)
    db.commit()
    
    
def create_bulk(db: Session, datas: list[RequestDataCreate], localidad_id:int):
    lista_de_objetos = [RequestDataCreate(**dicionario) for dicionario in datas]

    if not isinstance(datas, list):
        raise HTTPException(status_code=400, detail="Os dados devem ser uma lista")

    for Data in lista_de_objetos:    
        db_data = History_Data(Data)
        db_data.localidad_id = localidad_id
        db.add(db_data)
    db.commit()