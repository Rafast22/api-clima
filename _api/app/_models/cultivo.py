from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import Session, relationship
from ..database import Base
from datetime import datetime
from .._schemas.cultivo import RequestCultivoCreate, RequestCultivo
from .base_model import BaseModel
class Cultivo(BaseModel):
    __tablename__ = "Cultivos"

    create_date  = Column(DateTime, index=True, server_default=func.now(), default=func.now(), nullable=False)
    update_date = Column(DateTime, index=True, onupdate=func.now(), default=func.now(), nullable=False)
    name = Column(String, index=True, nullable=False)
    variety = Column(String, index=True, nullable=False)
    cycle_duration = Column(Integer, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    localidad_id = Column(Integer, ForeignKey('Localidad.id'))
    localidad = relationship("Localidad")

    @staticmethod
    def get_cultivos_usuario(db: Session, user_id: int):
        return db.query(Cultivo).filter(Cultivo.user_id == user_id).all()


