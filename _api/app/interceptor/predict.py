import pandas as pd
from pandas import DataFrame
from sklearn.tree import DecisionTreeRegressor
from .._models import nasa_data, predictions as pr
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
import pickle
import os

def load_dataframe(db:Session) -> DataFrame:
    db_data = nasa_data.get_historico(db)
    if not isinstance(db_data, list):
        # Crie um dicionário a partir do objeto
        data = dict(db_data)
    else:
        # Se for uma lista, use a solução anterior
        data = [dict(r) for r in db_data]
    data = [dict(r) for r in db_data]
    return pd.DataFrame.from_records(data)

def prepare_data(df):
    df = df.drop('localidad_id', axis=1)
    df = df.drop('id', axis=1)
    if "_sa_instance_state" in df.columns:
        df = df.drop('_sa_instance_state', axis=1)

    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d%H') 
    df = df.sort_values(by='date', ascending=True) 
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df = df.set_index("date")

    return df

def predict(db: Session):
    # engine = create_engine(SQLALCHEMY_DATABASE_URL)
    # SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 
    # db = get_db()
   
    # df = load_dataframe()
    db_data = nasa_data.get_historico(db)
    df = pd.DataFrame([vars(item) for item in db_data])
    df = prepare_data(df)

    prediction_date = 720
    prediction_date_last_day = 720
    train_data = df[prediction_date:]
    test_data = df[:-prediction_date]
    df = None
   
    # model = DecisionTreeRegressor(random_state=42)
    feature_list = ['year', 'month', 'day', 't2m', 'rh2m', 'prectotcorr', "qv2m", "ws2m"] 
    ignore_data_list = ['year', 'month', 'day'] 
    new_features = feature_list.copy()
    predictions = {}
    if not os.path.exists("models"):
        os.makedirs("models")

    for index, f in enumerate(feature_list):
        if f not in ignore_data_list:
                new_features = feature_list.copy() 
                new_features.remove(f)
                try:
                    model = pickle.load(open(f'models/model_{f}.sav', 'rb'))
                except FileNotFoundError:
                    

                    X_train = train_data[new_features]
                    y_train = train_data[f]

                    model = DecisionTreeRegressor(random_state=42)
                    model.fit(X_train, y_train)
                X_test = test_data[new_features][-prediction_date_last_day:]

                predictions[f] = model.predict(X_test).round(2)
                pickle.dump(model, open(f'models/model_{f}.sav', 'wb'))
    d={}

    # for paramter in predictions.keys():
    #     print(paramter.lower(), len(predictions[paramter].keys()))
    #     d[paramter.lower()] =list( predictions[paramter].values())
    # resultado = [dict(zip(predictions.keys(), valores)) for valores in zip(*predictions.values())]

    predictions["date"] = X_test.index
    df = pd.DataFrame.from_dict(predictions)

    # Convert 'date' column to datetime objects
    df['date'] = pd.to_datetime(df['date']) 

    # Format 'date' column as AAAAmmddHH
    df['date'] = df['date'].dt.strftime('%Y%m%d%H')

    pr.create_bulk(db, df.to_dict(orient='records'), 1)
