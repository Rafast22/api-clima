from datetime import datetime, date, timedelta
from collections import defaultdict
from typing import List
from .._models.predictions import Predictions
from .._models.localidad import Localidad
from .._models import predictions
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..interceptor import predict
from .._models.cultivo import Cultivo

def get_previcion(db: Session, fecha_inicial:date, fecha_final:date ,tipo, cultivo):
    db_predictions = predictions.get_previcion(db, fecha_inicial, fecha_final)
    if not db_predictions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pretict not found")
    

    result = defaultdict(list)  # Use defaultdict for efficiency and avoid key errors

    for obj in db_predictions:
        for attribute_name, attribute_value in obj.__dict__.items():
            if not callable(attribute_value) and not attribute_name.startswith('_'):
                if attribute_name == "date":
                    formato = "%Y%m%d%H"
                    data = datetime.strptime(attribute_value, formato)
                    result[attribute_name].append(data)
                else:
                    result[attribute_name].append(attribute_value)
    result["dia_optimo"] = list
    for k in range(0, len(result["id"])-1):
       result["dia_optimo"].append(get_valores_por_tipo_parametro_cosecha(result["prectotcorr"][k], result["ws2m"][k], result["rh2m"][k], result["t2m"][k], result["qv2m"][k], tipo, cultivo))

    return result

def get_previcion_by_day(db: Session, d:datetime):
    first_date = datetime(d.year, d.month, d.day)
    last_date = first_date + timedelta(hours=23)

    db_predictions = predictions.get_previcion_by_day(db,  first_date, last_date)

    result = defaultdict(list)  

    for obj in db_predictions:
        for attribute_name, attribute_value in obj.__dict__.items():
            if not callable(attribute_value) and not attribute_name.startswith('_'):
                if attribute_name == "date":
                    formato = "%Y%m%d%H"
                    data = attribute_value
                    result[attribute_name].append(data)
                else:
                    result[attribute_name].append(attribute_value)
    result["dia_optimo"] = list
    # for k in range(0, len(result["id"])-1):
    #    result["dia_optimo"].append(get_valores_por_tipo_parametro_cosecha(result["prectotcorr"][k], result["ws2m"][k], result["rh2m"][k], result["t2m"][k], result["qv2m"][k], tipo, cultivo))

    # return result
    return db_predictions

def get_previcion_total_from_today(db: Session, tipo:int, cultivo:int, localidad:int):
    today = datetime.now()
    fist_date = today.replace(day=1)

    db_predictions = predictions.get_previcion_by_day(db, fist_date, tipo, cultivo, localidad)

    # result = defaultdict(list)  

    # for obj in db_predictions:
    #     for attribute_name, attribute_value in obj.__dict__.items():
    #         if not callable(attribute_value) and not attribute_name.startswith('_'):
    #             if attribute_name == "date":
    #                 formato = "%Y%m%d%H"
    #                 data = datetime.strptime(attribute_value, formato)
    #                 result[attribute_name].append(data)
    #             else:
    #                 result[attribute_name].append(attribute_value)
    # result["dia_optimo"] = list
    # for k in range(0, len(result["id"])-1):
    #    result["dia_optimo"].append(get_valores_por_tipo_parametro_cosecha(result["prectotcorr"][k], result["ws2m"][k], result["rh2m"][k], result["t2m"][k], result["qv2m"][k], tipo, cultivo))

    # return result
    return db_predictions


def get_previcion_semana(db: Session, localidad:int):

    db_predictions = predictions.get_previcion_semana(db, localidad)
    data = [r.__dict__ for r in db_predictions]
    new_data = [{k: v for k, v in d.items() if k != 'id' and k != '_sa_instance_state'} for d in data]
    del data
    del db_predictions

    return new_data

def get_previcion_semana_by_data(db: Session, data_inicial:datetime, data_final:datetime, cultivo:Cultivo, localidad:Localidad):

    if data_final > data_inicial:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f" the date {str(data_final)} is greater than the date {str(data_inicial)}")


    db_predictions = predictions.get_previcion_semana_by_data(db, localidad, data_inicial, data_final)

    data = [r.__dict__ for r in db_predictions]
    # return pd.DataFrame.from_records(data)

    # df = pd.DataFrame.from_records(data)
    new_data = [{k: v for k, v in d.items() if k != 'id' and k != '_sa_instance_state'} for d in data]
    del data
    del db_predictions
    # columns = lambda lista: list(filter(lambda x: x != "date", lista))

    # mean = df[columns(df.columns.to_list())]
    # mean = df.groupby(df['date'].dt.date)[columns(df.columns.to_list())].mean()
    
    # mean = mean.map(lambda x: '{:.2f}'.format(x))
    # return mean.to_dict()

    


    # df['nota_plantio'] = df.apply(lambda x: calcular_nota(x, temp_ideal, precip_ideal, rad_ideal), axis=1)
    # df['porcentagem_plantio'] = df['nota_plantio'].apply(calcular_porcentagem)


    return new_data


def get_previcion_periodo(db: Session, data_inicio:datetime, data_fin:datetime, tipo:int, cultivo:int, localidad:int):
    try:
        db_predictions = predictions.get_previcion_periodo(db,  data_inicio, data_fin, localidad)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{str(ex)}")

    data = [r.__dict__ for r in db_predictions]
    new_data = [{k: v for k, v in d.items() if k != 'id' and k != '_sa_instance_state'} for d in data]
    del data
    del db_predictions
    return new_data
    #return predict.classify_day_type(new_data)
    # return new_data

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
