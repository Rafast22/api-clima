import pandas as pd
from pandas import DataFrame
from sklearn.tree import DecisionTreeRegressor
from .._models import nasa_data, predictions as pr, localidad
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
import pickle
import os
import numpy as np
from sklearn.model_selection import train_test_split
import xgboost as xgb
from dateutil.relativedelta import relativedelta
from datetime import timedelta, datetime
from sklearn.metrics import accuracy_score, precision_score
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

def predictA(db: Session, history_data, local: localidad.Localidad, update: bool = False):
    df = pd.DataFrame([item for item in history_data])
    df = prepare_data(df)  

    # prediction_horizon = 720
    first = history_data[-1]["Date"]
    last = first + relativedelta(months=6)
    horizon = last - first
    prediction_horizon = int(horizon.total_seconds() / 3600)
    train_data = df[:-prediction_horizon]
    test_data = df[-prediction_horizon:]

    feature_list = ['year', 'month', 'day', 'hour', 't2m', 'rh2m', 'prectotcorr', 'qv2m', 'ws2m']
    ignore_data_list = ['year', 'month', 'day', 'hour']

    predictions = {}

    for target in feature_list:
        if target not in ignore_data_list:
            new_features = [f for f in feature_list if f != target]
            X_train = train_data[new_features]
            y_train = train_data[target]
            X = df[new_features]
            y = df[target]
            # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            try:
                model = pickle.loads(getattr(local, f'model_{target}'))
                model.fit(X_train, y_train, xgb_model=model)

            except Exception as ex:
                model = xgb.XGBRegressor(random_state=42)
                model.fit(X_train, y_train)

            X_test = test_data[new_features]
            predictions[target] = model.predict(X_test).round(2)

            setattr(local, f'model_{target}', pickle.dumps(model))

    last_date = df.index[-1]
    date_range = pd.date_range(start=last_date + timedelta(hours=1), periods=prediction_horizon, freq='h')
    predictions['date'] = date_range

    predictions_df = pd.DataFrame(predictions)

    d = predictions_df.to_dict(orient='records')

    # if update:
    #     pr.delete_bulk_by_date(db, datetime.now(), [f for f in d].sort()[-1])
    local.last_request = history_data[-1]["Date"]
    localidad.update_entity(db, local)
    # pr.create_update_bulk(db, d, 1)
    # localidad.update_entity(db, local)
    pr.create_bulk(db, d, local.id)

def predict(db: Session, history_data, local: localidad.Localidad, update: bool = False):
    df = pd.DataFrame([item for item in history_data])
    df = prepare_data(df) 

    first = history_data[-1]["Date"]
    last = first + relativedelta(months=12)
    horizon = last - first
    prediction_horizon = int(horizon.total_seconds() / 3600)
    train_data = df[:-prediction_horizon]
    test_data = df[-prediction_horizon:]

    feature_list = ['year', 'month', 'day', 'hour', 't2m', 'rh2m', 'prectotcorr', 'qv2m', 'ws2m']
    ignore_data_list = ['year', 'month', 'day', 'hour']

    predictions = {}
    model_performance = {}
    for target in feature_list:
        if target not in ignore_data_list:
            new_features = [f for f in feature_list if f != target]
            X_train = train_data[new_features]
            y_train = train_data[target]
            X_test = test_data[new_features]
            y_test = test_data[target]  # Para avaliar o modelo

            try:
                model = pickle.loads(getattr(local, f'model_{target}'))
                model.fit(X_train, y_train, xgb_model=model)
            except Exception:
                model = xgb.XGBRegressor(random_state=42)
                model.fit(X_train, y_train)

            predictions[target] = model.predict(X_test).round(2)

            y_pred_train = model.predict(X_train).round(2)
            if target == 'prectotcorr':  
                y_train_bin = (y_train > 0.1).astype(int)  
                y_pred_bin = (y_pred_train > 0.1).astype(int)
                accuracy = accuracy_score(y_train_bin, y_pred_bin)
                precision = precision_score(y_train_bin, y_pred_bin, zero_division=0)
                model_performance[target] = {'accuracy': accuracy, 'precision': precision}

            setattr(local, f'model_{target}', pickle.dumps(model))

    last_date = df.index[-1]
    date_range = pd.date_range(start=last_date + timedelta(hours=1), periods=prediction_horizon, freq='h')
    predictions['date'] = date_range

    predictions_df = pd.DataFrame(predictions)

    def calculate_rain_probability(prectotcorr):
        prob = 1 / (1 + np.exp(-(prectotcorr - 0.1) * 10))  
        return np.clip(prob * 100, 0, 100).round(0)

    predictions_df['rain_probability'] = calculate_rain_probability(predictions_df['prectotcorr'])

    def calculate_forecast_confidence(prectotcorr, model_accuracy, model_precision):

        base_confidence = model_accuracy * 0.7 + model_precision * 0.3 
        confidence = base_confidence * (1 - np.exp(-prectotcorr)) 
        return np.clip(confidence * 100, 0, 100).round(2)

    prectotcorr_performance = model_performance.get('prectotcorr', {'accuracy': 0.8, 'precision': 0.7})  # Valores padrão
    predictions_df['forecast_confidence'] = calculate_forecast_confidence(
        predictions_df['prectotcorr'],
        prectotcorr_performance['accuracy'],
        prectotcorr_performance['precision']
    )

    d = predictions_df.to_dict(orient='records')

    local.last_request = history_data[-1]["Date"]
    localidad.update_entity(db, local)
    pr.create_bulk(db, d, local.id)

    del prectotcorr_performance, localidad
    
    return predictions_df   


def classify_day_type(data_to_predict:list):
    df = pd.DataFrame.from_dict(data_to_predict)
    df = df.sort_values(by='date', ascending=True) 

    return df.to_dict(orient='records')