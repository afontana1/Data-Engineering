import datetime
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine

from .config import get_config
from .forecast import get_forecast
from .measurments import get_measurments

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

def ingest_measurments(station: str, past_days: int) -> None:
    '''Get the measurments from wind station and ingest into db. Used only for monitoring and retraining.
    
    Args:
        station: string representing the name of the weather station.
        past_days: number of past days of measurments.'''     
    # Get data
    df = get_measurments(station, past_days)

    # Get database url
    db_url = get_config()

    # Create an SQLAlchemy engine
    engine = create_engine(db_url)

    # Define table name based on the station
    table_name = f'measurments_{station}'

    # Query the most recent date in the measurements table
    query = f'SELECT MAX("Time") as last_time FROM {table_name}'
    df_last = pd.read_sql(query, engine)

    # The result will be in the first row, first column of the DataFrame
    last_date_in_db = pd.to_datetime(df_last['last_time'].iloc[0])

    df_new_measurements = df[df['Time'] > last_date_in_db]

    # Check if there is new data to append
    if not df_new_measurements.empty:
        # Append new measurements to the database
        df_new_measurements.to_sql(table_name, engine, if_exists='append', index=False)
        print(f'New measurements for {station} ingested successfully into {table_name}.')
    else:
        print('No new measurements to ingest.')

def ingest_forecast() -> None:
    '''Get forecast for 3 days ahead and ingest into temp table in db. Used for inference.'''
    table_name = f'forecast_temp'
    
    # Get data
    df = get_forecast()

    # Get database url
    db_url = get_config()

    # Create an SQLAlchemy engine
    engine = create_engine(db_url)

    # Insert the Pandas DataFrame into the MySQL table
    try:
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f'Forecast for {df["Time"]} ingested successfully!')   
    except Exception as e:
        print(f"Data type mismatch or other data error: {e}")

def ingest_hist_forecast(past_days: int, forecast_days: int) -> None:
    '''Get past_days forecast and ingest into forecast. Used for monitoring and retraining.
    
    Args:
        past_days: number of past days of measurments.
        forecast_days: days of forecast into the future.'''   
    # Get forecast past_days into
    df = get_forecast(past_days, forecast_days)

    # Get database url
    db_url = get_config()

    # Create an SQLAlchemy engine
    engine = create_engine(db_url)

    # Fetch the last date in the forecast table
    last_date_query = f'SELECT MAX("Time") as last_time FROM forecast'
    df_last = pd.read_sql(last_date_query, engine)
    last_date_in_db = pd.to_datetime(df_last['last_time'].iloc[0])

    df_filtered = df[df['Time'] > last_date_in_db]
        
    if not df_filtered.empty:
        table_name = 'forecast'
        df_filtered.to_sql(table_name, engine, if_exists='append', index=False)
        print(f"Appended new forecast data from {last_date_in_db + datetime.timedelta(days=1)} to {datetime.date.today()} to the main table.")
    else:
        print("No new dates to append to the forecast table.")

def ingest_predictions_temp(station: str, pred: pd.DataFrame) -> None:
    '''Used for inference. Ingest predictions of the model to the RDS postgres.
       Args:
            station: string representing the name of the weather station.
            pred: pandas dataframe representing the model predictions.'''
    table_name = f'current_pred_{station}'
    
    # Get database url
    db_url = get_config()

    # Create an SQLAlchemy engine
    engine = create_engine(db_url)

    pred.to_sql(table_name, engine, if_exists='replace', index=False)
    print(f'Prediction for {station} ingested successfully!')

def record_training(station: str, model_name: str) -> None:
    '''Records the last retraining of the model to the RDS postgres.
       Args:
            station: string representing the name of the weather station.
            model_name: string representing the name of the retrained model.'''
    table_name = f'table_update_{station}'

    db_url = get_config()

    # Create an SQLAlchemy engine
    engine = create_engine(db_url)

    # Create a DataFrame with the necessary data
    df = pd.DataFrame({
        'model_name': [model_name],
        'retrained_date': [datetime.datetime.now().date()]  # Gets today's date
    })

    # Append the data to the SQL table
    df.to_sql(table_name, engine, if_exists='append', index=False)
    