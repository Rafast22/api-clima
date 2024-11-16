import datetime
from collections import defaultdict
from typing import  Annotated, List
from jwt.exceptions import InvalidTokenError
from ..database import SECRET_KEY, ALGORITHM
from .._models.nasa_data import History_Data
from ..database import oauth2_scheme
from .._models import nasa_data
from .._schemas.nasa_data import RequestData
from .._schemas.token import RequestToken, TokenData
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from .previcion import get_valores_por_tipo_parametro_cosecha

def get_historico_by_usuario(db: Session, tipo:int, cultivo:int) -> List[History_Data]:
    db_nasa_data = nasa_data.get_historico_by_usuario(db)
    if not db_nasa_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    

    result = defaultdict(list)  # Use defaultdict for efficiency and avoid key errors

    for obj in db_nasa_data:
        for attribute_name, attribute_value in obj.__dict__.items():
            if not callable(attribute_value) and not attribute_name.startswith('_'):
                if attribute_name == "date":
                    formato = "%Y%m%d%H"
                    data = datetime.datetime.strptime(attribute_value, formato)
                    result[attribute_name].append(data)
                else:
                    result[attribute_name].append(attribute_value)
    result["dia_optimo"] = []
    for k in range(0, len(result["id"])-1):
       result["dia_optimo"].append(get_valores_por_tipo_parametro_cosecha(result["prectotcorr"][k], result["ws2m"][k], result["rh2m"][k], result["t2m"][k], result["qv2m"][k], tipo, cultivo))
  
    return result

def get_historico_by_usuario_day(db: Session, day:str, cultivo:int, tipo:int) -> List[History_Data]:
    d = "".join("".join(day.split('-')).split("T")[0])

    db_nasa_data = nasa_data.get_historico_by_usuario_day(db, d)
    if not db_nasa_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    

    result = defaultdict(list)  
    
    for obj in db_nasa_data:
        for attribute_name, attribute_value in obj.__dict__.items():
            if not callable(attribute_value) and not attribute_name.startswith('_'):
                if attribute_name == "date":
                    formato = "%Y%m%d%H"
                    data = datetime.datetime.strptime(attribute_value, formato)
                    result[attribute_name].append(data)
                else:
                    result[attribute_name].append(attribute_value)
    result["dia_optimo"] = []
    for k in range(0, len(result["id"])-1):
       result["dia_optimo"].append(get_valores_por_tipo_parametro_cosecha(result["prectotcorr"][k], result["ws2m"][k], result["rh2m"][k], result["t2m"][k], result["qv2m"][k], tipo, cultivo))

    return result

