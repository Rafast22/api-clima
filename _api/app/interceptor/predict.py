import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from .._models import nasa_data
from ..database import get_db
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session


def predict(db: Session):
    # engine = create_engine(SQLALCHEMY_DATABASE_URL)
    # SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 
    # db = get_db()
    db_data = nasa_data.get_historico(db)
    if not isinstance(db_data, list):
        # Crie um dicionário a partir do objeto
        data = dict(db_data)
    else:
        # Se for uma lista, use a solução anterior
        data = [dict(r) for r in db_data]
    data = [dict(r) for r in db_data]
    df = pd.DataFrame.from_records(data)
    df = df.drop('localidad_id', axis=1)
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d%H') # formata la fecha de string a date time
    df = df.sort_values(by='date', ascending=True) # organiza la lista de datos por la fecha de forma ascendiente
    df.set_index("date")
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    prediction_point = 720
    prediction_point_last_day = 720
    train_data = df[prediction_point:]
    test_data = df[:-prediction_point]
    dictionary = {'year':"", 'month':"Mes", 'day':"Dia", 't2m':"Temperatura", 'rh2m':"Humedad Relativa", 'prectotcorr':"Precipitacion", "qv2m":"Humedad Especifica", "ws2m":"Velocidad del viento"}
    model = DecisionTreeRegressor(random_state=42)
    feature_list = ['year', 'month', 'day', 't2m', 'rh2m', 'prectotcorr', "qv2m", "ws2m"] # Lista de variables climaticas que seran calculadas por los modelos
    ignore_data_list = ['year', 'month', 'day'] #datos que no seran calculados
    new_features = feature_list.copy()
    for index, f in enumerate(feature_list):
        if f not in ignore_data_list:
                new_features = feature_list.copy() # Copia de la lista de variables para remover la variable a ser calculada para este valor de K
                new_features.remove(f)

                X_train = train_data[new_features]
                y_train = train_data[f]

                X_test = test_data[new_features][-prediction_point_last_day:] # obtiene los el ultimo dia de la prediccion para ser comparado con los valores previstos
                y_test = test_data[f]
                model.fit(X_train, y_train)
                predicted_y = model.predict(X_test)
                predicted_y = predicted_y.round(2)
                print(predicted_y)
