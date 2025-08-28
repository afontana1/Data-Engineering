from dotenv import load_dotenv
import os
import pandas as pd
import requests
import sys
from sqlalchemy import create_engine

# Load .env file
load_dotenv()

# Get the EC2 tracking server host from the environment variable
EC2_TRACKING_SERVER_HOST = os.getenv('EC2_TRACKING_SERVER_HOST')
EC2_ENDPOINT = f"http://{EC2_TRACKING_SERVER_HOST}:8000"

# Parameters for the RDS PostgreSQL instance
PG_HOST = os.getenv('PG_HOST')
PG_PORT = os.getenv('PG_PORT')
PG_DATABASE = os.getenv('PG_DATABASE')
PG_USER = os.getenv('PG_USER')
PG_PASSWORD = os.getenv('PG_PASSWORD')

# Create the MySQL database connection string
db_url = f'postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}'

engine = create_engine(db_url)

connection = engine.connect()

query = 'select * from model_versions'

df = pd.read_sql(query, connection)

max_version = df[df['name'] == 'xgboost-8features-hpt']['version'].max()
max_version_gust = df[df['name'] == 'xgboost-8features-hpt-guster3']['version'].max()
max_version_kuznica = df[df['name'] == 'xgboost-8features-hpt-kuznica']['version'].max()
max_version_gust_kuznica = df[df['name'] == 'xgboost-8features-hpt-guster-kuznica']['version'].max()

PARAMS_TEST = {
    "station": "rewa",
    "experiment_name": "xgb_aws_test3",
    "model_name": "xgboost-8features-hpt-test",
    "model_name_gust": "xgboost-8features-hpt-guster-test",
    "version": 1,
    "version_gust": 1,
    "mode": "base"
}


PARAMS_WIND_REWA = {
    "station": "rewa",
    "experiment_name": "xgb_aws_prod",
    "model_name": "xgboost-8features-hpt",
    "model_name_gust": "xgboost-8features-hpt-guster3",
    "version": str(max_version),
    "version_gust": str(max_version_gust),
    "mode": "base"
}

PARAMS_WIND_KUZNICA = {
    "station": "kuznica",
    "experiment_name": "xgb_aws_prod",
    "model_name": "xgboost-8features-hpt-kuznica",
    "model_name_gust": "xgboost-8features-hpt-guster-kuznica",
    "version": str(max_version_kuznica),
    "version_gust": str(max_version_gust_kuznica),
    "mode": "base"
}

PARAMS_GUST_REWA = {
    "station": "rewa",
    "experiment_name": "xgb_aws_prod",
    "model_name": "xgboost-8features-hpt-guster3",
    "model_name_gust": "xgboost-8features-hpt-guster3",
    "version": str(max_version_gust),
    "version_gust": str(max_version_gust),
    "mode": "gust"
}

PARAMS_GUST_KUZNICA = {
    "station": "kuznica",
    "experiment_name": "xgb_aws_prod",
    "model_name": "xgboost-8features-hpt-guster-kuznica",
    "model_name_gust": "xgboost-8features-hpt-guster-kuznica",
    "version": str(max_version_gust_kuznica),
    "version_gust": str(max_version_gust_kuznica),
    "mode": "gust"
}

connection.close()

def call_predict():
    response = requests.post(f'{EC2_ENDPOINT}/predict', json=PARAMS_WIND_REWA)
    print(response.text)

def call_monitor():
    response = requests.post(f'{EC2_ENDPOINT}/monitor', json=PARAMS_WIND_REWA)
    response = requests.post(f'{EC2_ENDPOINT}/monitor', json=PARAMS_GUST_REWA)
    print(response.text)

def call_retrain():
    response = requests.post(f'{EC2_ENDPOINT}/retrain', json=PARAMS_WIND_REWA)
    response = requests.post(f'{EC2_ENDPOINT}/retrain', json=PARAMS_GUST_REWA)
    print(response.text)

def call_predict_kuznica():
    response = requests.post(f'{EC2_ENDPOINT}/predict', json=PARAMS_WIND_KUZNICA)
    print(response.text)

def call_monitor_kuznica():
    response = requests.post(f'{EC2_ENDPOINT}/monitor', json=PARAMS_WIND_KUZNICA)
    response = requests.post(f'{EC2_ENDPOINT}/monitor', json=PARAMS_GUST_KUZNICA)
    print(response.text)

def call_retrain_kuznica():
    response = requests.post(f'{EC2_ENDPOINT}/retrain', json=PARAMS_WIND_KUZNICA)
    response = requests.post(f'{EC2_ENDPOINT}/retrain', json=PARAMS_GUST_KUZNICA)
    print(response.text)

def call_test():
    response = requests.post(f'{EC2_ENDPOINT}/retrain', json=PARAMS_TEST)
    response = requests.post(f'{EC2_ENDPOINT}/predict', json=PARAMS_TEST)
    response = requests.post(f'{EC2_ENDPOINT}/monitor', json=PARAMS_TEST)
    print(response.text)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python task_runner.py [predict|monitor|retrain]")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == 'predict':
        call_predict()
    elif command == 'monitor':
        call_monitor()
    elif command == 'retrain':
        call_retrain()
    elif command == 'predict_kuznica':
        call_predict_kuznica()
    elif command == 'monitor_kuznica':
        call_monitor_kuznica()
    elif command == 'retrain_kuznica':
        call_retrain_kuznica()
    elif command == 'test':
        call_test()
    else:
        print("Invalid command. Use 'predict', 'monitor', or 'retrain'.")