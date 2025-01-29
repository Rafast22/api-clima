from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Session
from ..database import Base
from .._schemas.localicad import RequestLocalidadCreate, RequestLocalidad
from fastapi import HTTPException, status

class Localidad(Base):
    __tablename__ = "Localidad"
    def __init__(self, localidad: RequestLocalidadCreate):
        
        self.latitude = localidad.latitude
        self.longitude = localidad.longitude
        self.user_id = localidad.user_id
        self.cultivo_id = localidad.cultivo_id
    
    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(String, index=True) 
    longitude = Column(String, index=True)
    user_id = Column(Integer, ForeignKey('User.id'))
    cultivo_id = Column(Integer, ForeignKey('Cultivos.id'), nullable=True)
   
    

def get_by_id(db: Session, localidad_id: int):
    return db.get(Localidad, localidad_id)

def get_by_user_id(db: Session, user_id: int):
    return db.query(Localidad).filter(Localidad.user_id == user_id)

def get_by_cultivo_id(db: Session, cultivo_id: int):
    return db.query(Localidad).filter(Localidad.cultivo_id == cultivo_id)

def create(db: Session, localidad: RequestLocalidadCreate):
    db_localidad = Localidad(localidad)
    db.add(db_localidad)
    db.commit()
    db.refresh(db_localidad)
    return db_localidad


def update(db: Session, localidad: RequestLocalidad):
    db_localidad = db.get(Localidad, localidad.id)
    if not db_localidad:
        raise None

    for key, value in vars(localidad).items():
        setattr(db_localidad, key, value)

    db.commit()
    db.refresh(db_localidad)
    return db_localidad

def delete(db: Session, user_id: int):
    db_localidad = db.get(Localidad, user_id)
    db.delete(db_localidad)
    db.commit()

