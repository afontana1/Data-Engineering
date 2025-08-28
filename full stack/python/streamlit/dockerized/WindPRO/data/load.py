import datetime
import pandas as pd
from datetime import date
from sqlalchemy import create_engine

from .config import get_config

def select_forecast(past_days=0, purpose='predict') -> pd.DataFrame:
    '''Get forecast for predictions or for monitoring from RDS postgres.

    Args:
        past_days: number of forecast days into the past.
        purpose: either predict, retrain or test.
    Returns:
        pandas dataframe representing the forecast.'''
    start_date = (datetime.datetime.now() - datetime.timedelta(days=past_days)).date()

    db_url = get_config()

    # Create an SQLAlchemy engine
    engine = create_engine(db_url)

    # Use the engine to connect to the database
    connection = engine.connect()
    
    if purpose == 'predict':
        query = f"SELECT * FROM forecast_temp"
    if purpose == 'test':
        query = f'''
                SELECT * FROM forecast
                WHERE "Time" >= '{start_date}';
                '''
    if purpose == 'retrain':
        query = f"SELECT * FROM forecast"

    # Use Pandas to read data from the database into a DataFrame
    df = pd.read_sql(query, connection)

    return df

def select_measurments(station: str, past_days=0, purpose='test') -> pd.DataFrame:
    '''Get measurments for monitoring or retraining from RDS postgres.
    
    Args:
        station: string representing the name of the weather station
        past_days: number of forecast days into the past.
        purpose: either predict, retrain or test.
    Returns:
        pandas dataframe representing the measurments from the weather station.'''
    start_date = (datetime.datetime.now() - datetime.timedelta(days=past_days)).date()

    db_url = get_config()

    # Create an SQLAlchemy engine
    engine = create_engine(db_url)

    # Use the engine to connect to the database
    connection = engine.connect()

    if purpose == 'retrain':
        query = f"SELECT * FROM measurments_{station}"
    if purpose == 'test':
            query = f'''
                    SELECT * FROM measurments_{station}
                    WHERE "Time" >= '{start_date}';
                    '''

    df = pd.read_sql(query, connection)

    return df

def select_training_date(station: str, model_name: str) -> pd.Timestamp:
    '''Get the date of the last model retraining.
    
    Args:
        station: string representing the name of the weather station.
        model_name: string representing name of the retrained model
    Returns:
        pandas dataframe representing the measurments from the weather station.'''
    db_url = get_config()

    # Create an SQLAlchemy engine
    engine = create_engine(db_url)

    # Use the engine to connect to the database
    connection = engine.connect()

    query = f"""
        SELECT retrained_date FROM table_update_{station}
        WHERE model_name = '{model_name}'
        ORDER BY retrained_date DESC
        LIMIT 1;
        """

    df = pd.read_sql(query, connection)

    last_date = df.iloc[0]['retrained_date']

    if isinstance(last_date, date):
        last_date = pd.to_datetime(last_date)

    connection.close()

    return last_date