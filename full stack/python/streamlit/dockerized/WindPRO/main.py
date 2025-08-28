import datetime
import pandas as pd
from typing import Tuple, List

from data.ingest import ingest_forecast, ingest_hist_forecast, ingest_measurments, record_training
from data.load import select_forecast, select_measurments, select_training_date
from models.model import Model

def predict(station: str, model_name: str, version: int, RUN_ID = None) -> Tuple[List[float], List, pd.Series]:
    '''
    Perform daily inference to predict wind speed. It ingests forecasts, selects relevant data,
    initializes the model, and makes predictions.

    Args:
        station: The station identifier.
        model_name: Name of the model to use.
        version: Version of the model.
        RUN_ID: Run ID for MLFlow tracking. Defaults to None.

    Returns:
        A tuple containing a list of predictions, a list of corresponding times, and a pandas Series of wind direction forecasts.
    '''
    ingest_forecast()
    df_forecast = select_forecast(purpose='predict')
    model = Model(station=station,RUN_ID=RUN_ID, model_name=model_name, version=version)
    time = df_forecast['Time'].tolist()
    direction = df_forecast['WindDirForecast']
    X = df_forecast[model.feature_names]
    return model.predict(X), time, direction

def monitor(station: str, model_name: str, version: int, RUN_ID: str = None, mode: str = 'base') -> Tuple[float, float]:
    '''
    Evaluate the model's performance every week by comparing predictions with actual measurements.

    Args:
        station: The station identifier.
        model_name: Name of the model to use.
        version: Version of the model.
        RUN_ID: Run ID for MLFlow tracking. Defaults to None.
        mode: The mode of operation for the model ('base' or 'gust'). Defaults to 'base'.

    Returns:
        A tuple containing the R2 score of the model predictions and the classic forecast data.
    '''
    last_training_date = select_training_date(station, model_name)
    difference = (datetime.datetime.now().date() - last_training_date.date()).days
    if difference == 0:
        past_days = 1
    else:
        past_days = difference

    ingest_hist_forecast(past_days=past_days, forecast_days=1)
    ingest_measurments(station=station, past_days=past_days)
    df_forecast = select_forecast(past_days=past_days, purpose='test')
    df_measurments = select_measurments(station, past_days=past_days, purpose='test')
    df_test = pd.merge(df_forecast, df_measurments, how='inner', on='Time')
    df_test.dropna(subset='WindSpeed', inplace=True)
    df_test.dropna(subset='WindGust', inplace=True)
    df_test.drop_duplicates(subset='Time', inplace=True)

    model = Model(station=station,RUN_ID=RUN_ID, model_name=model_name, version=version)
    return model.model_evaluation(df_test, mode)

def retrain(station: str, model_name: str, version: int, RUN_ID: str = None, mode: str = 'base') -> float:
    '''
    Retrain the model every month. This process includes data loading, transformation, parameter tuning,
    fitting, and model saving. It returns the training cross-validation score.

    Args:
        station: The station identifier.
        model_name: Name of the model to use.
        version: Version of the model.
        RUN_ID: Run ID for MLFlow tracking. Defaults to None.
        mode: The mode of operation for the model ('base' or 'gust'). Defaults to 'base'.

    Returns:
        float: The mean accuracy score from k-fold cross-validation during training.
    '''
    model = Model(station=station,RUN_ID=RUN_ID, model_name=model_name, version=version)
    df_forecast = select_forecast(purpose='retrain')
    df_measurments = select_measurments(station, purpose='retrain')
    model.transform(df_forecast, df_measurments, mode)  
    del df_forecast
    del df_measurments
    model.parameter_tuning() 
    train_cv_accuracy = model.k_fold_cross_validation()
    model.fit()
    model.save_model()
    record_training(station, model_name)
    del model
    return train_cv_accuracy