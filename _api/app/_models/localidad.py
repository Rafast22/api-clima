from sqlalchemy import Column, Integer, String, Boolean, DateTime, or_, ForeignKey, Numeric 
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, Session
from sqlalchemy.ext.declarative import declarative_base
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
    latitude = Column(String, index=True) #models.DecimalField(max_digits=100, decimal_places=15, null=True)
    longitude = Column(String, index=True) #models.DecimalField(max_digits=100, decimal_places=2, null=True)
    user_id = Column(Integer, ForeignKey('User.id'))
    cultivo_id = Column(Integer, ForeignKey('Cultivos.id'), nullable=True)
    # user = relationship("User", back_populates="localidad") 
    # cultivo = relationship("Cultivos", back_populates="localidad") 
    

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
    if db_localidad is None:
        raise None

    for key, value in vars(localidad).items():
        setattr(db_localidad, key, value)

    db.commit()
    db.refresh(db_localidad)
    return db_localidad

def delete(db: Session, user_id: int):
    db_localidad = db.get(Localidad, user_id)
    if not db_localidad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Localidad not found")
    db.delete(db_localidad)
    db.commit()

