from sqlalchemy import Column, Integer, String, Boolean, DateTime, or_, ForeignKey, DECIMAL, and_
from sqlalchemy.sql import func, between
from sqlalchemy.orm import Session, load_only
from sqlalchemy.ext.declarative import declarative_base
from ..database import Base
from .._schemas.nasa_data import RequestDataCreate, RequestData
from fastapi import HTTPException, status
from datetime import datetime, timedelta, date
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
    db.bulk_save_objects(data)
    db.commit()
    
    
def create_bulk(db: Session, datas: list[RequestDataCreate], localidad_id:int):
    lista_de_objetos = [RequestDataCreate(**dicionario) for dicionario in datas]

    if not isinstance(datas, list):
        raise HTTPException(status_code=400, detail="Os dados devem ser uma lista")

    for data in lista_de_objetos:
            existing_record = (db.query(Predictions).filter(Predictions.date == data.date).first())

            if existing_record:
                [setattr(existing_record, key, value) for key, value in vars(data).items() ]
                db.add(existing_record)

            else:
                new_record = Predictions(data)
                new_record.localidad_id = localidad_id
                db.add(new_record)


    db.commit()

def delete_bulk_by_date(db: Session, first_date: datetime, last_date:datetime):

    db.query(Predictions).filter(Predictions.date.between(first_date, last_date)
                                 ).delete(synchronize_session=False)
    db.commit()

def get_previcion(db: Session, fecha_inicial:datetime, fecha_final:datetime):
    db_data = db.query(Predictions).limit(250).all()

    if not db_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Predictions not found")
    return db_data

def get_previcion_by_day(db: Session, first_date:datetime, last_date:datetime):
    # db_data = db.query(Predictions).filter(
    #     func.lower(Predictions.date).startswith(day)
    # ).all()

    db_data = db.query(Predictions
                       ).options(load_only(Predictions.id, 
                       Predictions.date, 
                       Predictions.prectotcorr, 
                       Predictions.rh2m, 
                       Predictions.qv2m, 
                       Predictions.t2m, 
                       Predictions.ws2m
                        )).filter(Predictions.date.between(first_date, last_date)).all()
                        # )).filter(Predictions.date == day).all()

    return db_data

def get_previcion_total_from_today(db: Session, day:datetime, tipo:int, cultivo:int, localidad:int):
    db_data = db.query(Predictions
                       ).options(load_only(Predictions.id, 
                       Predictions.date, 
                       Predictions.prectotcorr, 
                       Predictions.rh2m, 
                       Predictions.qv2m, 
                       Predictions.t2m, 
                       Predictions.ws2m
                        # )).filter(Predictions.date.between(day, dt_final)).all()
                        )).filter(and_(Predictions.date > day, Predictions.tipo == tipo, 
                                       Predictions.cultivo == cultivo, 
                                       Predictions.localidad_id == localidad )).all()

    return db_data


def get_previcion_semana(db: Session, localidad:int):
    # dt_inicio = datetime.strptime(day, '%Y%m%d%H')
    # dt_final = dt_inicio + timedelta(days=6, hours=23)
    d = datetime.now()
    day = datetime(d.year, d.month, d.day)
    # dia_da_semana = day.weekday()
    # primeira_dia = day - timedelta(days=(dia_da_semana + 1) % 7, hours=0, minutes=0, milliseconds=0)
    # dt_final = primeira_dia + timedelta(days=5, hours=23, minutes=59, milliseconds=59)
    dt_final = day + timedelta(days=7, hours=23, minutes=59, milliseconds=59)

    db_data = db.query(Predictions
                       ).options(load_only(Predictions.id, 
                       Predictions.date, 
                       Predictions.prectotcorr, 
                       Predictions.rh2m, 
                       Predictions.qv2m, 
                       Predictions.t2m, 
                       Predictions.ws2m
                        # )).filter(Predictions.date.between(day, dt_final)).all()
                        )).filter(and_(Predictions.date.between(day, dt_final), 
                                        Predictions.localidad_id == localidad)).all()
    return db_data

def get_previcion_semana_by_data(db: Session, localidad:int, data_inicial:datetime, data_final:datetime):


    db_data = db.query(Predictions
                       ).options(load_only(Predictions.id, 
                       Predictions.date, 
                       Predictions.prectotcorr, 
                       Predictions.rh2m, 
                       Predictions.qv2m, 
                       Predictions.t2m, 
                       Predictions.ws2m
                        # )).filter(Predictions.date.between(day, dt_final)).all()
                        )).filter(and_(Predictions.date.between(data_inicial, data_final), 
                                        Predictions.localidad_id == localidad)).all()
    return db_data


def get_previcion_periodo(db: Session, data_inicio:datetime, data_fin:datetime, localidad:int):

    db_data = db.query(Predictions
                       ).options(load_only(Predictions.id, 
                       Predictions.date, 
                       Predictions.prectotcorr, 
                       Predictions.rh2m, 
                       Predictions.qv2m, 
                       Predictions.t2m, 
                       Predictions.ws2m
                        )).filter(and_(Predictions.date.between(data_inicio, data_fin), 
                                        Predictions.localidad_id == localidad)).all()
    return db_data