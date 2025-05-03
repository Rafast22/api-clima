from sqlalchemy import Column, Integer, DateTime, ForeignKey, DECIMAL, Double
from .base_model import BaseModel
class BasePrediction(BaseModel):
    __abstract__ = True  
    date = Column(DateTime)
    prectotcorr = Column(DECIMAL(10, 3))
    rh2m = Column(DECIMAL(10, 3))
    qv2m = Column(DECIMAL(10, 3))
    t2m = Column(DECIMAL(10, 3))
    ws2m = Column(DECIMAL(10, 3))
    ps = Column(DECIMAL(10, 3))
    model_accuracy = Column(Double)
    probability_rain = Column(DECIMAL(5, 2))
    localidad_id = Column(Integer, ForeignKey('Localidad.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('User.id'))
    
