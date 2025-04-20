import datetime
from collections import defaultdict
from typing import  Annotated, List
from .._models.historico import History 
from .._models.user import User
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from .._schemas.paginated import PaginationResponse

def get_historico_by_usuario(db: Session, user:User, page: int = 1, per_page: int = 10):
    db_nasa_data = History.get_all_by_user_paginated(db, user.id, page, per_page)
    # result = defaultdict(list)  # Use defaultdict for efficiency and avoid key errors

    # for obj in db_nasa_data:
    #     for attribute_name, attribute_value in obj.__dict__.items():
    #         if not callable(attribute_value) and not attribute_name.startswith('_'):
    #             if attribute_name == "date":
    #                 formato = "%Y%m%d%H"
    #                 data = datetime.datetime.strptime(attribute_value, formato)
    #                 result[attribute_name].append(data)
    #             else:
    #                 result[attribute_name].append(attribute_value)
    # result["dia_optimo"] = []
    # for k in range(0, len(result["id"])-1):
    #    result["dia_optimo"].append(get_valores_por_tipo_parametro_cosecha(result["prectotcorr"][k], result["ws2m"][k], result["rh2m"][k], result["t2m"][k], result["qv2m"][k], tipo, cultivo))
  
    return db_nasa_data

# def get_historico_by_usuario(db: Session):

#     db_nasa_data = History.get_all_by_user_paginated(db, d)
#     if not db_nasa_data:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    

#     result = defaultdict(list)  
    
#     for obj in db_nasa_data:
#         for attribute_name, attribute_value in obj.__dict__.items():
#             if not callable(attribute_value) and not attribute_name.startswith('_'):
#                 if attribute_name == "date":
#                     formato = "%Y%m%d%H"
#                     data = datetime.datetime.strptime(attribute_value, formato)
#                     result[attribute_name].append(data)
#                 else:
#                     result[attribute_name].append(attribute_value)
#     result["dia_optimo"] = []
#     # for k in range(0, len(result["id"])-1):
#     #    result["dia_optimo"].append(get_valores_por_tipo_parametro_cosecha(result["prectotcorr"][k], result["ws2m"][k], result["rh2m"][k], result["t2m"][k], result["qv2m"][k], tipo, cultivo))

#     return result

