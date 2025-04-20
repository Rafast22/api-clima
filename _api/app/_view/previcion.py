from datetime import datetime, date, timedelta
from .._models.localidad import Localidad
from .._models import predictions
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .._models.cultivo import Cultivo
import pandas as pd
from dateutil.relativedelta import relativedelta
from ..interceptor.predict import _classify_day_harvest, _classify_day_planting

def db_data_to_dict(db_data):
    data = [r.__dict__ for r in db_data]
    new_data = [{k: v for k, v in d.items() if k != 'id' and k != '_sa_instance_state'} for d in data]
    return new_data

def get_previcion_by_day(db: Session, d:datetime):
    first_date = datetime(d.year, d.month, d.day)
    last_date = first_date + timedelta(hours=23)

    db_predictions = predictions.get_previcion_by_day(db,  first_date, last_date)
    # new_data = db_data_to_dict(db_predictions)
    return db_predictions

def get_previcion_semana(db: Session, localidad:int):

    db_predictions = predictions.get_previcion_semana(db, localidad)
    # data = [r.__dict__ for r in db_predictions]
    # new_data = [{k: v for k, v in d.items() if k != 'id' and k != '_sa_instance_state'} for d in data]
    new_data = db_data_to_dict(db_predictions)

    del db_predictions
    df = pd.DataFrame.from_dict(new_data)
    if "localidad_id" in df.columns:
        df = df.drop('localidad_id', axis=1) 
    
    if "user_id" in df.columns:
        df = df.drop('user_id', axis=1) 
    

    def change_v(row):
        model_accuracy = row['model_accuracy']
        probability_rain = row['probability_rain']
        return (model_accuracy > 70)
    df['info'] = df.apply(change_v, axis=1)
    return df.to_dict(orient='records')

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

# def get_previcion_periodo(db: Session, data_inicio:datetime, data_fin:datetime, tipo:int, cultivo:int, localidad:int):
#     try:
#         db_predictions = predictions.get_previcion_periodo(db,  data_inicio, data_fin, localidad)
#     except Exception as ex:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{str(ex)}")

#     data = [r.__dict__ for r in db_predictions]
#     new_data = [{k: v for k, v in d.items() if k != 'id' and k != '_sa_instance_state'} for d in data]
#     del data
#     del db_predictions
#     return new_data
#     #return predict.classify_day_type(new_data)
#     # return new_data

def get_previcion_total_from_today(db: Session, tipo:int, cultivo:int, localidad:int):
    today = datetime.now()
    fist_date = today.replace(day=1)

    db_predictions = predictions.get_previcion_by_day(db, fist_date, tipo, cultivo, localidad)

    return db_predictions

def get_perfet_days(db: Session, user_id:int, cultivo: int, tipo: int, data_inicial, data_final):
   
    db_predictions = predictions.get_perfet_days(db, data_inicial, data_final, user_id)
    if len(db_predictions) == 0:
        return []
    df = pd.DataFrame.from_records([row.__dict__ for row in db_predictions])
    if "localidad_id" in df.columns:
        df = df.drop('localidad_id', axis=1) 
    if "_sa_instance_state" in df.columns:
        df = df.drop('_sa_instance_state', axis=1) 
    if "user_id" in df.columns:
        df = df.drop('user_id', axis=1) 
    if "id" in df.columns:
        df = df.drop('id', axis=1) 


    # if "localidad_id" in df.columns:
    #     df = df.drop('localidad_id', axis=1) 
    if cultivo == 1:
        cul = "trigo" 
    elif cultivo == 2:
        cul = "mais"
    elif cultivo == 3:
        cul = "soja"

    df['index'] =  df['date']
    df.set_index('index', inplace=True)
    mean_predictions = df.groupby(pd.Grouper(freq='D'))[['t2m', "rh2m", "prectotcorr", "qv2m", "ws2m"]].mean()

    if tipo == 2:
        mean_predictions['perfect'] = mean_predictions.apply(lambda row: _classify_day_planting(row, cul), axis=1)
    else:
        mean_predictions['perfect'] = mean_predictions.apply(lambda row: _classify_day_harvest(row, cul), axis=1)
    mean_predictions['date'] = mean_predictions.index
    del db_predictions
 
    mean_predictions =  mean_predictions[['date', 'perfect']]
    return mean_predictions.to_dict(orient='records')

def get_first_and_last_day_alternative(a: date) -> tuple[date, date]:
  first_day = date(a.year, a.month, 1)
  next_month = first_day + relativedelta(months=1)
  last_day = next_month - relativedelta(days=1)
  return first_day, last_day

