import pandas as pd
from .._models.predictions import Predictions
from .._models.localidad import Localidad
import pickle
from scipy.stats import norm

import numpy as np
from sklearn.model_selection import train_test_split
import xgboost as xgb
from dateutil.relativedelta import relativedelta
from datetime import timedelta, datetime
from sklearn.metrics import accuracy_score, precision_score
from sklearn.metrics import accuracy_score, precision_score, mean_absolute_error, root_mean_squared_error, mean_squared_error
from scipy.special import expit

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

def train_xgb_model(X_train, y_train, existing_model=None):
    if existing_model:
        model = pickle.loads(existing_model)
    else:
        model = xgb.XGBRegressor(
            random_state=100,
            learning_rate=0.05,
            n_estimators=200,
            max_depth=6,
            colsample_bytree=0.8,
            subsample=0.8
        )
    
    model.fit(X_train, y_train)
    
    return model

def calculate_rain_probability_expanded(df):
    prob = 0
    peso_precipitacao = 0.1
    peso_temperatura = -0.15
    peso_umidade_relativa = 0.2
    peso_umidade_especifica = 0.3
    peso_vento = -0.05
    precip_norm = df['prectotcorr'] / df['prectotcorr'].max() if df['prectotcorr'].max() > 0 else 0
    temp_norm = (df['t2m'] - df['t2m'].min()) / (df['t2m'].max() - df['t2m'].min()) if (df['t2m'].max() - df['t2m'].min()) > 0 else 0.5
    ur_norm = df['rh2m'] / 100
    ue_norm = df['qv2m'] / df['qv2m'].max() if df['qv2m'].max() > 0 else 0
    vento_norm = df['ws2m'] / df['ws2m'].max() if df['ws2m'].max() > 0 else 0

    prob += peso_precipitacao * precip_norm
    prob += peso_temperatura * temp_norm
    prob += peso_umidade_relativa * ur_norm
    prob += peso_umidade_especifica * ue_norm
    prob += peso_vento * vento_norm

    prob = np.clip(prob, 0, 1) * 100
    return prob.round(0)

def predict(db, history_data, local:Localidad, update=False):
    
    df = pd.DataFrame(history_data)
    df = prepare_data(df)  
    
    first = history_data[-1]["Date"]
    last = first + relativedelta(months=12)
    horizon = int((last - first).total_seconds() / 3600)

    feature_list = ['year', 'month', 'day', 'hour', 't2m', 'rh2m', 'prectotcorr', 'qv2m', 'ws2m', 'ps']
    ignore_data_list = ['year', 'month', 'day', 'hour']

    train_data, test_data = train_test_split(df, test_size=horizon / len(df), shuffle=False)

    predictions = {}
    accuracy_list = {}
    model_performance = {}
    new_features = ['t2m', 'rh2m', 'prectotcorr', 'qv2m', 'ws2m', 'ps']
    for target in feature_list:
        if target not in ignore_data_list:
            new_features = [f for f in new_features if f != target]
            X_train, y_train = train_data[new_features], train_data[target]
            X_test, y_test = test_data[new_features], test_data[target]
            model = train_xgb_model(X_train, y_train, getattr(local, f'model_{target}', None))
            y_pred = model.predict(X_test).round(2)
            y_pred_train = model.predict(X_train).round(2)
            
            predictions[target] = y_pred

            accuracy_list[f"{target}_accuracy"] = calculate_accuracy(y_test, y_pred)

            if target == 'prectotcorr':  
                predictions[target] = np.where(predictions[target] < 0, 0, predictions[target]).round(2)

                y_pred_train = np.maximum(y_pred_train, 0)
                y_train_bin, y_pred_bin = (y_train > 0.1).astype(int), (y_pred_train > 0.1).astype(int)
                accuracy = accuracy_score(y_train_bin, y_pred_bin)
                precision = precision_score(y_train_bin, y_pred_bin, zero_division=0)
                model_performance[target] = {'accuracy': accuracy, 'precision': precision}

            setattr(local, f'model_{target}', pickle.dumps(model))
            del y_pred, X_test, X_train, y_test, y_train,
    predictions['date'] = pd.date_range(start=df.index[-1] + timedelta(hours=1), periods=horizon, freq='h')

    predictions_df = pd.DataFrame(predictions)

    accuracy_list = pd.DataFrame(accuracy_list)
    # predictions_df = predictions_df[[k for k in predictions.keys() if 'accuracy' not in k ]]

    predictions_df['model_accuracy'] = accuracy_list.apply(calculate_accuracy_mean, axis=1)

    
    predictions_df['probability_rain'] = calculate_rain_probability_expanded(predictions_df)
    
    local.last_request = history_data[-1]["Date"]
    Localidad.update(local, db)
    Predictions.create_bulk(db, local.id, predictions_df.to_dict(orient='records'))

    return predictions_df

def calculate_accuracy(test_y, pre_y):
    with np.errstate(divide='ignore', invalid='ignore'):
        relative_error = np.abs(test_y - pre_y) / np.abs(test_y)
    cond_zero = np.abs(test_y) < 1e-8
    acc_percentual = np.where(
        cond_zero,
        np.where(np.abs(pre_y) < 1e-8, 100.0, 0.0),
        100 * (1 - relative_error)
    )

    return acc_percentual

def calculate_accuracy_mean(row):
    np_array = row.to_numpy()
    return np.mean(np_array)

def gaussian_score(value, ranges):
    score = 0.0
    for (min_val, max_val, sigma) in ranges:
        mean = (min_val + max_val) / 2
        if min_val <= value <= max_val:
            score = max(score, norm.pdf(value, mean, sigma) / norm.pdf(mean, mean, sigma))
    return score

def _classify_day_harvest(row, crop_type):
    t2m_media = row['t2m']
    rh2m_media = row['rh2m']
    prectotcorr_media = row['prectotcorr']
    qv2m_media = row['qv2m']
    ws2m_media = row['ws2m']

    thresholds = {
        'soja': {
            't2m': [(25, 30, 2.5), (20, 25, 2.0), (15, 20, 1.5), (30, 35, 2.0), (35, 40, 1.5)],
            'rh2m': [(50, 60, 2.0), (45, 50, 1.5), (40, 45, 1.0), (60, 65, 1.5), (65, 70, 1.0)],
            'prectotcorr': [(0, 2, 1.5), (2, 5, 1.0), (5, 10, 0.5), (10, 15, 0.0)],
            'qv2m': [(8, 11, 2.0), (7, 8, 1.5), (6, 7, 1.0), (11, 13, 1.5), (13, 15, 1.0)],
            'ws2m': [(0, 3, 1.5), (3, 5, 1.0), (5, 7, 0.5)]
        },
        'mais': {
            't2m': [(25, 32, 2.5), (20, 25, 2.0), (15, 20, 1.5), (32, 35, 2.0), (35, 38, 1.5)],
            'rh2m': [(50, 60, 2.0), (45, 50, 1.5), (40, 45, 1.0), (60, 65, 1.5), (65, 70, 1.0)],
            'prectotcorr': [(0, 1, 1.5), (1, 3, 1.0), (3, 8, 0.5), (8, 15, 0.0)],
            'qv2m': [(9, 12, 2.0), (8, 9, 1.5), (7, 8, 1.0), (12, 14, 1.5), (14, 16, 1.0)],
            'ws2m': [(0, 3, 1.5), (3, 5, 1.0), (5, 7, 0.5)]
        },
        'trigo': {
            't2m': [(15, 20, 2.5), (12, 15, 2.0), (10, 12, 1.5), (20, 25, 2.0), (25, 28, 1.5)],
            'rh2m': [(50, 70, 2.0), (45, 50, 1.5), (40, 45, 1.0), (70, 75, 1.5), (75, 80, 1.0)],
            'prectotcorr': [(0, 2, 1.5), (2, 5, 1.0), (5, 10, 0.5), (10, 15, 0.0)],
            'qv2m': [(7, 10, 2.0), (6, 7, 1.5), (5, 6, 1.0), (10, 12, 1.5), (12, 14, 1.0)],
            'ws2m': [(0, 5, 1.5), (5, 7, 1.0), (7, 9, 0.5)]
        },
        'default': {
            't2m': [(20, 28, 2.5), (18, 20, 2.0), (15, 18, 1.5), (28, 32, 2.0), (32, 35, 1.5)],
            'rh2m': [(50, 70, 2.0), (45, 50, 1.5), (40, 45, 1.0), (70, 80, 1.5), (80, 85, 1.0)],
            'prectotcorr': [(0, 2, 1.5), (2, 5, 1.0), (5, 10, 0.5), (10, 15, 0.0)],
            'qv2m': [(8, 11, 2.0), (7, 8, 1.5), (6, 7, 1.0), (11, 13, 1.5), (13, 15, 1.0)],
            'ws2m': [(0, 4, 1.5), (4, 6, 1.0), (6, 8, 0.5)]
        }
    }

    if crop_type in thresholds:
        crop_thresholds = thresholds[crop_type]
    else:
        print(f"Aviso: Cultura '{crop_type}' não reconhecida. Usando valores genéricos.")
        crop_thresholds = thresholds['default']


    weights = {'t2m': 0.3, 'rh2m': 0.25, 'prectotcorr': 0.2, 'qv2m': 0.15, 'ws2m': 0.1}
    score = 0.0
    score += integrated_gaussian_score(t2m_media, crop_thresholds['t2m']) * weights['t2m']
    score += integrated_gaussian_score(rh2m_media, crop_thresholds['rh2m']) * weights['rh2m']
    score += integrated_gaussian_score(prectotcorr_media, crop_thresholds['prectotcorr']) * weights['prectotcorr']
    score += integrated_gaussian_score(qv2m_media, crop_thresholds['qv2m']) * weights['qv2m']
    score += integrated_gaussian_score(ws2m_media, crop_thresholds['ws2m']) * weights['ws2m']

    percentage = score * 100 / sum(weights.values())

    return min(max(percentage, 0), 100)

def _classify_day_planting(row, crop_type):
    t2m_media = row['t2m']
    rh2m_media = row['rh2m']
    prectotcorr_media = row['prectotcorr']
    qv2m_media = row['qv2m']
    ws2m_media = row['ws2m']

    thresholds = {
        'soja': {
            't2m': [(20, 30, 2.5), (18, 20, 2.0), (15, 18, 1.5), (32, 35, 1.5)],
            'rh2m': [(60, 80, 2.0), (55, 60, 1.5), (50, 55, 1.0), (80, 85, 1.5), (85, 90, 1.0)],
            'prectotcorr': [(2, 10, 1.5), (0, 2, 1.0), (10, 15, 1.0), (15, 20, 0.5)],
            'qv2m': [(8, 12, 2.0), (7, 8, 1.5), (6, 7, 1.0), (12, 14, 1.5), (14, 16, 1.0)],
            'ws2m': [(0, 4, 1.5), (4, 6, 1.0), (6, 8, 0.5)]
        },
        'mais': {
            't2m': [(25, 32, 2.5), (20, 25, 2.0), (18, 20, 1.5), (32, 35, 2.0), (35, 38, 1.5)],
            'rh2m': [(65, 85, 2.0), (60, 65, 1.5), (55, 60, 1.0), (85, 90, 1.5), (90, 95, 1.0)],
            'prectotcorr': [(5, 15, 1.5), (2, 5, 1.0), (15, 20, 1.0), (20, 25, 0.5)],
            'qv2m': [(9, 13, 2.0), (8, 9, 1.5), (7, 8, 1.0), (13, 15, 1.5), (15, 17, 1.0)],
            'ws2m': [(0, 3, 1.5), (3, 5, 1.0), (5, 7, 0.5)]
        },
        'trigo': {
            't2m': [(15, 20, 2.5), (12, 15, 2.0), (10, 12, 1.5), (20, 25, 2.0), (25, 28, 1.5)],
            'rh2m': [(50, 70, 2.0), (45, 50, 1.5), (40, 45, 1.0), (70, 75, 1.5), (75, 80, 1.0)],
            'prectotcorr': [(2, 8, 1.5), (0, 2, 1.0), (8, 12, 1.0), (12, 15, 0.5)],
            'qv2m': [(7, 10, 2.0), (6, 7, 1.5), (5, 6, 1.0), (10, 12, 1.5), (12, 14, 1.0)],
            'ws2m': [(0, 5, 1.5), (5, 7, 1.0), (7, 9, 0.5)]
        },
        'default': {
            't2m': [(18, 28, 2.5), (15, 18, 2.0), (12, 15, 1.5), (28, 32, 2.0), (32, 35, 1.5)],
            'rh2m': [(60, 80, 2.0), (55, 60, 1.5), (50, 55, 1.0), (80, 90, 1.5), (90, 95, 1.0)],
            'prectotcorr': [(2, 10, 1.5), (0, 2, 1.0), (10, 15, 1.0), (15, 20, 0.5)],
            'qv2m': [(8, 12, 2.0), (6, 8, 1.5), (5, 6, 1.0), (12, 14, 1.5), (14, 16, 1.0)],
            'ws2m': [(0, 4, 1.5), (4, 6, 1.0), (6, 8, 0.5)]
        }
    }

    if crop_type in thresholds:
        crop_thresholds = thresholds[crop_type]
    else:
        print(f"Aviso: Cultura '{crop_type}' não reconhecida. Usando valores genéricos.")
        crop_thresholds = thresholds['default']

    weights = {'t2m': 0.3, 'rh2m': 0.25, 'prectotcorr': 0.2, 'qv2m': 0.15, 'ws2m': 0.1}
    score = 0.0
    # score += gaussian_score(t2m_media, crop_thresholds['t2m']) * weights['t2m']
    # score += gaussian_score(rh2m_media, crop_thresholds['rh2m']) * weights['rh2m']
    # score += gaussian_score(prectotcorr_media, crop_thresholds['prectotcorr']) * weights['prectotcorr']
    # score += gaussian_score(qv2m_media, crop_thresholds['qv2m']) * weights['qv2m']
    # score += gaussian_score(ws2m_media, crop_thresholds['ws2m']) * weights['ws2m']

    score += integrated_gaussian_score(t2m_media, crop_thresholds['t2m']) * weights['t2m']
    score += integrated_gaussian_score(rh2m_media, crop_thresholds['rh2m']) * weights['rh2m']
    score += integrated_gaussian_score(prectotcorr_media, crop_thresholds['prectotcorr']) * weights['prectotcorr']
    score += integrated_gaussian_score(qv2m_media, crop_thresholds['qv2m']) * weights['qv2m']
    score += integrated_gaussian_score(ws2m_media, crop_thresholds['ws2m']) * weights['ws2m']


    percentage = score * 100 / sum(weights.values())

    return min(max(percentage, 0), 100)

def integrated_gaussian_score(value, ranges):
    score = 0.0
    for min_val, max_val, sigma in ranges:
        mean = (min_val + max_val) / 2
        if min_val <= value <= max_val:
            lower_cdf = norm.cdf(min_val, mean, sigma)
            upper_cdf = norm.cdf(max_val, mean, sigma)
            max_cdf = norm.cdf(mean, mean, sigma)
            if max_cdf > 0:
                score = max(score, (upper_cdf - lower_cdf) / (2 * max_cdf))
            elif lower_cdf == upper_cdf and lower_cdf == 0.5:
                score = 1.0
    return score


