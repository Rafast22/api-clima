from sqlalchemy import Column, Integer, String, Boolean, DateTime, or_, ForeignKey, DECIMAL, and_
from sqlalchemy.sql import func, between
from sqlalchemy.orm import Session, load_only
from sqlalchemy.ext.declarative import declarative_base
from .._schemas.nasa_data import RequestDataCreate, RequestData
from fastapi import HTTPException, status
from datetime import datetime, timedelta
from ._base_prediction import BasePrediction
from typing import List, Dict, Union
class Predictions(BasePrediction):
    __tablename__ = "Predictions"

    @classmethod
    def create_bulk(cls, db: Session, localidad_id: int, datas: List[Union[Dict, RequestDataCreate]]):
        if not isinstance(datas, list):
            raise HTTPException(status_code=400, detail="Os dados devem ser uma lista")

        for data in datas:
            date_to_check = data['date'] if isinstance(data, dict) else data.model_dump().get('date')
            existing_record = db.query(cls).filter(cls.date == date_to_check).first()

            if existing_record:
                data_dict = data if isinstance(data, dict) else data.model_dump()
                for key, value in data_dict.items():
                    setattr(existing_record, key, value)
                db.add(existing_record)
            else:
                if isinstance(data, dict):
                    new_record = cls(**data)
                else:
                    new_record = cls(**data.model_dump())
                new_record.localidad_id = localidad_id
                db.add(new_record)
        db.commit()
        return len(datas)
def gravar_bulk(db: Session, data: list[RequestDataCreate]):
    db.bulk_save_objects(data)
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
    db_data = db.query(Predictions
                       ).options(load_only(Predictions.id, 
                       Predictions.date, 
                       Predictions.prectotcorr, 
                       Predictions.rh2m, 
                       Predictions.qv2m, 
                       Predictions.t2m, 
                       Predictions.ws2m
                        )).filter(Predictions.date.between(first_date, last_date)).all()

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
                        )).filter(and_(Predictions.date > day, Predictions.tipo == tipo, 
                                       Predictions.cultivo == cultivo, 
                                       Predictions.localidad_id == localidad )).all()

    return db_data


def get_previcion_semana(db: Session, localidad:int):
    d = datetime.now()
    day = datetime(d.year, d.month, d.day)
    dt_final = day + timedelta(days=7, hours=23, minutes=59, milliseconds=59)

    db_data = db.query(Predictions
                       ).filter(
                            Predictions.date.between(day, dt_final), 
                                        # Predictions.localidad_id == localidad
                                        ).all()
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
                        )).filter(and_(Predictions.date.between(data_inicial, data_final), 
                                        Predictions.localidad_id == localidad)).all()
    return db_data


def get_perfet_days(db: Session, data_inicial:datetime, data_final:datetime, user_id: int):

    db_data = db.query(Predictions).filter(Predictions.date.between(data_inicial, data_final)).all()
    return db_data