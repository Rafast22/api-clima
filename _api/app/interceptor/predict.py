import pandas as pd
from pandas import DataFrame
from sklearn.tree import DecisionTreeRegressor
from .._models import nasa_data, predictions as pr, localidad
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
import pickle
import os
from sklearn.model_selection import train_test_split
import xgboost as xgb
from dateutil.relativedelta import relativedelta
from datetime import timedelta, datetime
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

def predict(db: Session, history_data, local: localidad.Localidad, update: bool = False):
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

# def predict(db: Session, history_data: List[Dict], local: localidad.Localidad, update: bool = False):
#     # Converter os dados do banco em um DataFrame
#     db_data = history_data
#     df = pd.DataFrame([item for item in db_data])
#     df = prepare_data(df)  # Supondo que prepare_data seja uma função existente para pré-processamento

#     # Verificar a última data disponível nos dados de treinamento
#     last_date = pd.to_datetime(df[['year', 'month', 'day', 'hour']]).iloc[-1]
#     print(f"Última data disponível nos dados de treinamento: {last_date}")

#     # Criar datas futuras para previsão (720 horas a partir da última data)
#     future_dates = pd.date_range(start=str(last_date + timedelta(hours=1)), periods=720, freq='H')
#     future_df = pd.DataFrame({'Date': future_dates})
#     future_df['year'] = future_df['Date'].dt.year
#     future_df['month'] = future_df['Date'].dt.month
#     future_df['day'] = future_df['Date'].dt.day
#     future_df['hour'] = future_df['Date'].dt.hour

#     # Preencher as features futuras com valores médios (ou outra lógica)
#     for col in ['rh2m', 'qv2m', 't2m', 'prectotcorr', 'ws2m']:
#         future_df[col] = df[col].mean()

#     # Feature Engineering: Adicionar lags e features temporais
#     for col in ['t2m', 'rh2m', 'prectotcorr', 'qv2m', 'ws2m']:
#         df[f'{col}_lag1'] = df[col].shift(1)  # Lag de 1 hora
#         future_df[f'{col}_lag1'] = future_df[col].shift(1)

#     # Remover NaNs gerados pelos lags
#     df = df.dropna()

#     # Definir features e targets
#     feature_list = ['year', 'month', 'day', 'hour', 't2m', 'rh2m', 'prectotcorr', 'qv2m', 'ws2m', 't2m_lag1', 'rh2m_lag1', 'prectotcorr_lag1', 'qv2m_lag1', 'ws2m_lag1']
#     ignore_data_list = ['year', 'month', 'day', 'hour']
#     predictions = {}

#     # Treinar e prever para cada target
#     for target in feature_list:
#         if target not in ignore_data_list:
#             new_features = [f for f in feature_list if f != target]  # Remover o target das features

#             # Carregar o modelo salvo ou treinar um novo
#             try:
#                 model = pickle.loads(getattr(local, f'model_{target}'))
#             except Exception as ex:
#                 # Dividir os dados em treino e teste
#                 X = df[new_features]
#                 y = df[target]
#                 X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#                 # Treinar o modelo XGBoost
#                 model = XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
#                 model.fit(X_train, y_train)

#                 # Salvar o modelo treinado
#                 setattr(local, f'model_{target}', pickle.dumps(model))

#             # Fazer previsões para o futuro
#             predictions[target] = model.predict(future_df[new_features]).round(2)

#     # Adicionar as datas futuras ao dicionário de previsões
#     predictions["date"] = future_dates

#     # Converter as previsões em um DataFrame
#     df_predictions = pd.DataFrame.from_dict(predictions)

#     # Atualizar o banco de dados
#     local.last_request = datetime.now()
#     if update:
#         pr.delete_bulk_by_date(db, datetime.now(), df_predictions['date'].max())
#     localidad.update_entity(db, local)
#     pr.create_update_bulk(db, df_predictions.to_dict(orient='records'), 1)

#     # Retornar as previsões (opcional)
#     return df_predictions


# com o xvboot
# def predict(db: Session, history_data: List[Dict], local: localidad.Localidad, update: bool = False):
#     # Converter os dados do banco em um DataFrame
#     db_data = history_data
#     df = pd.DataFrame([item for item in db_data])
#     df = prepare_data(df)  # Supondo que prepare_data seja uma função existente para pré-processamento

#     # Definir o período de previsão (720 horas = 30 dias)
#     prediction_date = 720

#     # Criar datas futuras para previsão
#     future_dates = pd.date_range(start='2023-10-01', end='2023-10-31', freq='H')
#     future_df = pd.DataFrame({'Date': future_dates})
#     future_df['year'] = future_df['Date'].dt.year
#     future_df['month'] = future_df['Date'].dt.month
#     future_df['day'] = future_df['Date'].dt.day
#     future_df['hour'] = future_df['Date'].dt.hour

#     # Preencher as features futuras com valores médios (ou outra lógica)
#     for col in ['rh2m', 'qv2m', 't2m', 'prectotcorr', 'ws2m']:
#         future_df[col] = df[col].mean()

#     # Feature Engineering: Adicionar lags e features temporais
#     for col in ['t2m', 'rh2m', 'prectotcorr', 'qv2m', 'ws2m']:
#         df[f'{col}_lag1'] = df[col].shift(1)  # Lag de 1 hora
#         future_df[f'{col}_lag1'] = future_df[col].shift(1)

#     # Remover NaNs gerados pelos lags
#     df = df.dropna()

#     feature_list = ['year', 'month', 'day', 'hour', 't2m', 'rh2m', 'prectotcorr', 'qv2m', 'ws2m', 't2m_lag1', 'rh2m_lag1', 'prectotcorr_lag1', 'qv2m_lag1', 'ws2m_lag1']
#     ignore_data_list = ['year', 'month', 'day', 'hour']
#     predictions = {}

#     for target in feature_list:
#         if target not in ignore_data_list:
#             # new_features = [f for f in feature_list if f != target]  # Remover o target das features

#             try:
#                 # model = pickle.loads(getattr(local, f'model_{target}'))
#                 raise
#             except Exception as ex:
#                 X = df[feature_list]
#                 y = df[target]
#                 X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#                 model = XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
#                 model.fit(X_train, y_train)

#                 # setattr(local, f'model_{target}', pickle.dumps(model))

#             predictions[target] = model.predict(future_df[feature_list]).round(2)

#     predictions["date"] = future_dates

#     df_predictions = pd.DataFrame.from_dict(predictions)

#     local.last_request = datetime.now()
#     if update:
#         pr.delete_bulk_by_date(db, datetime.now(), df_predictions['date'].max())
#     localidad.update_entity(db, local)
#     pr.create_update_bulk(db, df_predictions.to_dict(orient='records'), 1)

#     # Limpar variáveis não utilizadas
#     del df, future_df, predictions, df_predictions

# def predict(db: Session, history_data, local: localidad.Localidad, update: bool = False):
#     db_data = history_data
#     df = pd.DataFrame([item for item in db_data])
#     df = prepare_data(df)

#     # Criar datas futuras para previsão
#     future_dates = pd.date_range(start='2025-02-01', end='2025-02-28', freq='h')
#     future_df = pd.DataFrame({'Date': future_dates})
#     future_df['year'] = future_df['Date'].dt.year
#     future_df['month'] = future_df['Date'].dt.month
#     future_df['day'] = future_df['Date'].dt.day
#     future_df['hour'] = future_df['Date'].dt.hour

#     # Adicionar lags e tendências
#     df['time'] = (df['Date'] - df['Date'].min()).dt.days
#     future_df['time'] = (future_df['Date'] - df['Date'].min()).dt.days

#     # Prever tendências para features futuras
#     for feature in ['t2m', 'rh2m', 'qv2m', 'prectotcorr', 'ws2m']:
#         model_trend = LinearRegression()
#         model_trend.fit(df[['time']], df[feature])
#         future_df[feature] = model_trend.predict(future_df[['time']])

#     # Adicionar lags
#     for lag in [1, 24]:  # Lag de 1 hora e 24 horas
#         for feature in ['t2m', 'rh2m', 'qv2m', 'prectotcorr', 'ws2m']:
#             df[f'{feature}_lag{lag}'] = df[feature].shift(lag)
#             future_df[f'{feature}_lag{lag}'] = df[feature].iloc[-lag]

#     # Preencher valores NaN
#     df.fillna(method='bfill', inplace=True)

#     # Treinar e prever
#     feature_list = ['year', 'month', 'day', 'hour', 't2m', 'rh2m', 'prectotcorr', "qv2m", "ws2m"]
#     ignore_data_list = ['year', 'month', 'day', 'hour']
#     predictions = {}

#     for target in feature_list:
#         if target not in ignore_data_list:
#             try:
#                 model = pickle.loads(getattr(local, f'model_{target}'))
#             except Exception as ex:
#                 X = df[feature_list]
#                 y = df[target]
#                 X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#                 model = DecisionTreeRegressor(random_state=42)
#                 model.fit(X_train, y_train)

#             predictions[target] = model.predict(future_df[feature_list])
#             setattr(local, f'model_{target}', pickle.dumps(model))

#     # Salvar resultados
#     predictions["date"] = future_df['Date']
#     df_predictions = pd.DataFrame.from_dict(predictions)
#     local.last_request = datetime.now()
#     d = df_predictions.to_dict(orient='records')

#     if update:
#         pr.delete_bulk_by_date(db, datetime.now(), [f for f in d].sort()[-1])
#     localidad.update_entity(db, local)
#     pr.create_update_bulk(db, d, 1)

def classify_day_type(data_to_predict:list):
    df = pd.DataFrame.from_dict(data_to_predict)
    df = df.sort_values(by='date', ascending=True) 

    return df.to_dict(orient='records')

def update_model_data(db: Session,history_data ,local:localidad.Localidad, ):

    predict(db, history_data, local, True)

def classify_day_type(data_to_predict:list):
    df = pd.DataFrame.from_dict(data_to_predict)
    df = df.sort_values(by='date', ascending=True) 

    return df.to_dict(orient='records')