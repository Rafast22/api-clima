from sqlalchemy import Column, Integer, String, Boolean, DateTime, or_, ForeignKey, DECIMAL
from sqlalchemy.sql import func, between
from sqlalchemy.orm import relationship, Session
from sqlalchemy.ext.declarative import declarative_base
from ..database import Base
from .._schemas.nasa_data import RequestDataCreate, RequestData
from fastapi import HTTPException, status
from datetime import datetime, timedelta
class Predictions(Base):
    __tablename__ = "Predictions"
    def __init__(self, history: RequestDataCreate):
        self.date = history.date
        self.prectotcorr = history.prectotcorr
        self.rh2m = history.rh2m
        self.qv2m = history.qv2m
        self.t2m = history.t2m
        self.ws2m = history.ws2m

    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=True)
    prectotcorr = Column(DECIMAL(10, 3), nullable=True)
    rh2m = Column(DECIMAL(10, 3), nullable=True)
    qv2m = Column(DECIMAL(10, 3), nullable=True)
    t2m = Column(DECIMAL(10, 3), nullable=True)
    ws2m = Column(DECIMAL(10, 3), nullable=True)
    localidad_id = Column(Integer, ForeignKey('Localidad.id'), nullable=False)
    

def get_by_id(db: Session, Data_id: int):
    return db.get(Predictions, Data_id)

def create(db: Session, Data: RequestDataCreate):
    db_data = Predictions(Data)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

def update(db: Session, Data: RequestData):
    db_data = db.get(Predictions, Data.id)
    if db_data is None:
        raise None

    for key, value in vars(Data).items():
        setattr(db_data, key, value)

    db.commit()
    db.refresh(db_data)
    return db_data

def delete(db: Session, user_id: int):
    db_data = db.get(Predictions, user_id)
    if not db_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Predictions not found")
    db.delete(db_data)
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
        db_data = Predictions(Data)
        db_data.localidad_id = localidad_id
        db.add(db_data)
    db.commit()

def get_previcion(db: Session, fecha_inicial:datetime, fecha_final:datetime):
    # db_data = db.query(Predictions).filter(Predictions.user_id == user_id)
    db_data = db.query(Predictions).limit(250).all()

    if not db_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Predictions not found")
    return db_data

def get_previcion_by_day(db: Session, day:str):
    # db_data = db.query(Predictions).filter(Predictions.user_id == user_id)
    db_data = db.query(Predictions).filter(
        func.lower(Predictions.date).startswith(day)  # Filtra pelo nome começando com "maria"
    ).all()

    if not db_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Predictions not found")
    return db_data

def get_previcion_semana(db: Session, day:str):
    dt_inicio = datetime.strptime(day, '%Y%m%d%H')
    # dt_final = datetime.strptime(data_inicio, '%Y%m%d%H')
    dt_final = dt_inicio + timedelta(days=6, hours=23)

    db_data = db.query(Predictions).filter(
        between(
            func.cast(
                func.substring(Predictions.date, 1, 4) + '-' +
                func.substring(Predictions.date, 5, 2) + '-' +
                func.substring(Predictions.date, 7, 2) + ' ' +
                func.substring(Predictions.date, 9, 2) + ':00:00',
                DateTime
            ),
            dt_inicio,
            dt_final
        )
    ).all()


    if not db_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Predictions not found")
    return db_data