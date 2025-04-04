from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary, DateTime, and_
from sqlalchemy.orm import Session, relationship 
from ..database import Base
from .._schemas.localidad import RequestLocalidadCreate, RequestLocalidad
from fastapi import HTTPException, status
from .base_model import BaseModel
from .cultivo import Cultivo
class Localidad(BaseModel):
    __tablename__ = "Localidad"

    latitude = Column(String, index=True) 
    longitude = Column(String, index=True)
    model_prectotcorr = Column(LargeBinary)
    model_rh2m = Column(LargeBinary)
    model_qv2m = Column(LargeBinary)
    model_t2m = Column(LargeBinary)
    model_ws2m = Column(LargeBinary)
    last_request = Column(DateTime)
    user_id = Column(Integer, ForeignKey('User.id'))
    predictions = relationship("Predictions", cascade="all, delete-orphan", passive_deletes=True)
    
    @staticmethod
    def get_by_latitude_longitude(db: Session, latitude: str, longitude: str):
        return db.query(Localidad).filter(and_(Localidad.latitude == latitude, Localidad.longitude == longitude)).all()
   
    @staticmethod
    def get_by_user_id(db: Session, user_id: int):
        return db.query(Localidad).filter(Localidad.user_id == user_id).all()
    
    @staticmethod
    def get_by_cultivo_id(db: Session, cultivo_id: int):
        cultivo = db.query(Cultivo).filter(Cultivo.id == cultivo_id).first()
        if cultivo: 
            if cultivo.localidad_id:
                return db.query(Localidad).filter(Localidad.id == cultivo.localidad_id).first()
            raise HTTPException(status_code=status.HTTP_302_FOUND, detail='Cultivo found but not has Localidad')
            
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Cultivo not found')


    
