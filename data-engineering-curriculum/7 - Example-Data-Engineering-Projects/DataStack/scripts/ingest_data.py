from dotenv import load_dotenv
import os
import pandas as pd
from sqlalchemy import create_engine
import time
import sys


def main():
    
    load_dotenv('.env')
    
    user = os.environ.get('MY_SQL_USER')
    password = os.environ.get('MY_SQL_PASSWORD')
    host = os.environ.get('MY_SQL_HOST')
    port = os.environ.get('MY_SQL_PORT')
    db = os.environ.get('MY_SQL_DATABASE')
    table_name = os.environ.get('MY_SQL_TABLE_NAME')

    time.sleep(15)
    
    print(f'mysql+pymysql://{user}:{password}@{host}:{port}/{db}')
    sys.stdout.flush()

    engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{db}')
    pd.io.parquet.get_engine('auto')
    print('Reading data...')
    sys.stdout.flush()
    df = pd.read_parquet('./data/jan-2021/green_tripdata_2022-01.parquet')
    print('Inserting data...')
    sys.stdout.flush()
    df.to_sql(name=table_name, con=engine, if_exists='append')


if __name__ == '__main__':
    
    main()