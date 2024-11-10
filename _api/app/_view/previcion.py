import datetime
from collections import defaultdict
from typing import  Annotated, List
from jwt.exceptions import InvalidTokenError
from ..database import SECRET_KEY, ALGORITHM
from .._models.predictions import Predictions
from .._models import predictions
from .._schemas.token import RequestToken, TokenData
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from ..interceptor import predict
def start_predict(db: Session) :
    predict.predict(db)


def get_previcion(db: Session, fecha_inicial:datetime.date, fecha_final:datetime.date ,tipo, cultivo) -> List[Predictions]:
    db_predictions = predictions.get_previcion(db, fecha_inicial, fecha_final)
    if not db_predictions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pretict not found")
    

    result = defaultdict(list)  # Use defaultdict for efficiency and avoid key errors

    for obj in db_predictions:
        for attribute_name, attribute_value in obj.__dict__.items():
            if not callable(attribute_value) and not attribute_name.startswith('_'):
                if attribute_name == "date":
                    formato = "%Y%m%d%H"
                    data = datetime.datetime.strptime(attribute_value, formato)
                    result[attribute_name].append(data)
                else:
                    result[attribute_name].append(attribute_value)
    result["dia_optimo"] = list
    for k in range(0, len(result["id"])-1):
       result["dia_optimo"].append(get_valores_por_tipo_parametro_cosecha(result["prectotcorr"][k], result["ws2m"][k], result["rh2m"][k], result["t2m"][k], result["qv2m"][k], tipo, cultivo))

    return result

def get_previcion_by_day(db: Session, day:str, tipo, cultivo) -> List[Predictions]:
    d = "".join("".join(day.split('-')).split("T")[0])

    db_predictions = predictions.get_previcion_by_day(db,  day)
    if not db_predictions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    

    result = defaultdict(list)  

    for obj in db_predictions:
        for attribute_name, attribute_value in obj.__dict__.items():
            if not callable(attribute_value) and not attribute_name.startswith('_'):
                if attribute_name == "date":
                    formato = "%Y%m%d%H"
                    data = datetime.datetime.strptime(attribute_value, formato)
                    result[attribute_name].append(data)
                else:
                    result[attribute_name].append(attribute_value)
    result["dia_optimo"] = list
    for k in range(0, len(result["id"])-1):
       result["dia_optimo"].append(get_valores_por_tipo_parametro_cosecha(result["prectotcorr"][k], result["ws2m"][k], result["rh2m"][k], result["t2m"][k], result["qv2m"][k], tipo, cultivo))

    return result

def get_valores_por_tipo_parametro_cosecha(prectotcorr, ws2m, rh2m, t2m, qv2m, tipo, cultivo)->bool:
    
    
    
    if tipo==1: #Cosecha
        if cultivo == 1: #"trigo"
            if 20 <= t2m <= 30 and rh2m <= 70 and prectotcorr <= 5:
                return True
        elif cultivo == 2: #"soja"
            if 20 <= t2m <= 40 and rh2m <= 70  and prectotcorr <= 5 and ws2m >= 1.8:
                return True
        elif cultivo == 3:  #"maiz"
            if 24 <= t2m <= 30 and 60 <= rh2m <= 70 and prectotcorr <= 5 and ws2m <= 1.5:
                return True
        return False
    elif tipo==2: #SImebra
        if cultivo == 1: #"trigo"
            if 15 <= t2m <= 25 and rh2m >= 70 and prectotcorr >= 10:
                return True
        elif cultivo == 2: #"soja"
            if 20 <= t2m <= 30 and rh2m >= 70 and prectotcorr >= 15 and ws2m <= 1:
                return True
        elif cultivo == 3:  #"maiz"
            if 25 <= t2m <= 35 and qv2m >= 70 and prectotcorr >= 10 and ws2m <= 1:
                return True
        return False




    # if tipo==1: #Cosecha
    #     if cultivo == 1: #"trigo"
    #         if 24 <= t2m <= 36 and rh2m <= 70 and prectotcorr <= 5:
    #             return True
    #     elif cultivo == 2: #"soja"
    #         if 25 <= t2m and rh2m <= 75  and prectotcorr <= 5 and ws2m >= 1.8:
    #             return True
    #     elif cultivo == 3:  #"maiz"
    #         if 26 >= t2m and qv2m >= 10 and prectotcorr >= 5 and ws2m <= 2:
    #             return True
    #     return False
    # elif tipo==2:
    #     if cultivo == 1: #"trigo"
    #         if 15 <= t2m <= 25 and rh2m >= 60 and prectotcorr >= 5:
    #             return True
    #     elif cultivo == 2: #"soja"
    #         if 20 <= t2m <= 30 and rh2m >= 70 and prectotcorr >= 10 and ws2m <= 20:
    #             return True
    #     elif cultivo == 3:  #"maiz"
    #         if 25 <= t2m <= 35 and qv2m >= 10 and prectotcorr >= 5 and ws2m <= 15:
    #             return True
    #     return False


def calcula_media_semanal(prectotcorr, ws2m, rh2m, t2m, qv2m):
    
    for p in range(len(prectotcorr)):
        pass
