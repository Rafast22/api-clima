import pandas as pd
from pandas import DataFrame
from sklearn.tree import DecisionTreeRegressor
from .._models import nasa_data, predictions as pr, localidad
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
import pickle
import os

def load_dataframe(db:Session) -> DataFrame:
    db_data = nasa_data.get_historico(db)
    if not isinstance(db_data, list):
        data = dict(db_data)
    else:
        data = [dict(r) for r in db_data]
    data = [dict(r) for r in db_data]
    return pd.DataFrame.from_records(data)

def prepare_data(df):
    if "localidad_id" in df.columns:
        df = df.drop('localidad_id', axis=1)

    if "id" in df.columns:
        df = df.drop('localidad_id', axis=1)

    if "_sa_instance_state" in df.columns:
        df = df.drop('_sa_instance_state', axis=1)

    df = df.sort_values(by='Date', ascending=True) 
    df['year'] = df['Date'].dt.year
    df['month'] = df['Date'].dt.month
    df['day'] = df['Date'].dt.day
    df['hour'] = df['Date'].dt.hour
    df = df.set_index("Date")

    return df

def predict(db: Session, history_data, local:localidad.Localidad):
    db_data = history_data
    df = pd.DataFrame([item for item in db_data])
    df = prepare_data(df)
    prediction_date = 720
    test = df[-prediction_date:]
    df = df[:-prediction_date]
    train_data = df[:-prediction_date]
    test_data = df[prediction_date:]
    del df
   
    feature_list = ['year', 'month', 'day', 'hour', 't2m', 'rh2m', 'prectotcorr', "qv2m", "ws2m"] 
    ignore_data_list = ['year', 'month', 'day', 'hour'] 
    new_features = feature_list.copy()
    predictions = {}

    for index, f in enumerate(feature_list):
        if f not in ignore_data_list:
                new_features = feature_list.copy() 
                new_features.remove(f)
                try:
                    model = pickle.loads(getattr(local, f'model_{f}'))
                except Exception as ex :

                    X_train = train_data[new_features]
                    y_train = train_data[f]

                    model = DecisionTreeRegressor(random_state=42)
                    model.fit(X_train, y_train)
                X_test = test[new_features]

                predictions[f] = model.predict(X_test).round(2)
                setattr(local, f'model_{f}', pickle.dumps(model))

    predictions["date"] = X_test.index
    df = pd.DataFrame.from_dict(predictions)

    localidad.update_entity(db, local)
    pr.create_bulk(db, df.to_dict(orient='records'), 1)

def classify_day_type(data_to_predict:list):
    df = pd.DataFrame.from_dict(data_to_predict)
    df = df.sort_values(by='date', ascending=True) 

    return df.to_dict(orient='records')