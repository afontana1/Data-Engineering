import os
import pandas as pd
from sqlalchemy import create_engine

from config import get_config

def migrate(station: str) -> None:
    '''Migrate data for a station from mysql to postgres.'''
    # Get database url
    db_url = get_config()

    # Create an SQLAlchemy engine
    engine = create_engine(db_url)

    connection = engine.connect()

    query1 = f"SELECT * FROM forecast"
    query2 = f"SELECT * FROM measurments_{station}"

    df_forecast = pd.read_sql(query1, connection)
    df_measurments = pd.read_sql(query2, connection)

    # Parameters for the RDS PostgreSQL instance
    PG_HOST = os.environ.get('PG_HOST')
    PG_PORT = os.environ.get('PG_PORT')
    PG_DATABASE = os.environ.get('PG_DATABASE')
    PG_USER = os.environ.get('PG_USER')
    PG_PASSWORD = os.environ.get('PG_PASSWORD')

    pg_engine = create_engine(f'postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}')

    # Ingest data from df_forecast into PostgreSQL table
    df_forecast.to_sql('forecast', con=pg_engine, if_exists='replace', index=False)

    # Ingest data from df_measurments into PostgreSQL table
    df_measurments.to_sql(f'measurments_{station}', con=pg_engine, if_exists='replace', index=False)

    pg_engine.dispose()

if __name__ == '__main__': 
    migrate('rewa')