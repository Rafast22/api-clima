from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary, DateTime, and_
from sqlalchemy.orm import Session, relationship 
from ..database import Base
from .._schemas.localidad import RequestLocalidadCreate, RequestLocalidad
from fastapi import HTTPException, status

class Localidad(Base):
    __tablename__ = "Localidad"

    def __init__(self, localidad: RequestLocalidadCreate):
        
        self.latitude = localidad.latitude
        self.longitude = localidad.longitude
        self.user_id = localidad.user_id
        self.cultivo_id = localidad.cultivo_id if localidad.cultivo_id else None

    
    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(String, index=True) 
    longitude = Column(String, index=True)
    user_id = Column(Integer, ForeignKey('User.id', ondelete="CASCADE"), nullable=True)
    model_prectotcorr = Column(LargeBinary, nullable=True)
    model_rh2m = Column(LargeBinary, nullable=True)
    model_qv2m = Column(LargeBinary, nullable=True)
    model_t2m = Column(LargeBinary, nullable=True)
    last_request = Column(DateTime, nullable=True)
    model_ws2m = Column(LargeBinary, nullable=True)
    predictions = relationship("Predictions", cascade="all, delete-orphan", passive_deletes=True)
    
   
    

def get_by_id(db: Session, localidad_id: int):
    return db.get(Localidad, localidad_id)

def get_by_latitude_longitude(db: Session, latitude: str, longitude: str):
    return db.query(Localidad).filter(
        and_(Localidad.latitude == latitude, Localidad.longitude == longitude)
                                      ).first()


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

def update_entity(db: Session, localidad:Localidad):
    db_localidad = db.get(Localidad, localidad.id)

    db.add(db_localidad)
    db.commit()
   

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

