from sqlalchemy import Column, Integer, String, Boolean, DateTime, or_, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, Session
from sqlalchemy.ext.declarative import declarative_base
from ..database import Base
from .._schemas.cultivo import RequestCultivoCreate, RequestCultivo
from fastapi import HTTPException, status


class Cultivo(Base):
    __tablename__ = "Cultivos"
    id = Column(Integer, primary_key=True, index=True)
    create_date  = Column(DateTime, index=True, server_default=func.now(), nullable=False)
    update_date = Column(DateTime, index=True, onupdate=func.now(), nullable=False)
    name = Column(String, index=True, nullable=False)
    variety = Column(String, index=True, nullable=False)
    cycle_duration = Column(Integer, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)

def get_cultivo_by_id(db: Session, cultivo_id: int):
    return db.get(Cultivo, cultivo_id)

def get_cultivos_usuario(db: Session, user_id: int):
    return db.query(Cultivo).filter(Cultivo.user_id == user_id)

def create_cultivo(db: Session, cultivo: RequestCultivoCreate):
    db_cultivo = Cultivo(cultivo)
    db.add(db_cultivo)
    db.commit()
    db.refresh(db_cultivo)
    return db_cultivo

def update_cultivo(db: Session, cultivo: RequestCultivo):
    db_cultivo = db.get(Cultivo, cultivo.id)
    if db_cultivo is None:
        raise None

    for key, value in vars(cultivo).items():
        setattr(db_cultivo, key, value)

    db.commit()
    db.refresh(db_cultivo)
    return db_cultivo

def delete_cultivo(db: Session, user_id: int):
    db_cultivo = db.get(Cultivo, user_id)
    if not db_cultivo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cultivo not found")
    db.delete(db_cultivo)
    db.commit()

