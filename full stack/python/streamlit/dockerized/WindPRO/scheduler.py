from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator

default_args = {
    'owner': 'me',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'fastapi_endpoints',
    default_args=default_args,
    description='Schedule FastAPI Endpoints',
    schedule_interval=None,
    start_date=datetime.today(),
    catchup=False,
)

predict_task = SimpleHttpOperator(
    task_id='predict_task',
    method='POST',
    http_conn_id='fastapi_conn',
    endpoint='/predict',
    dag=dag,
)

monitor_task = SimpleHttpOperator(
    task_id='monitor_task',
    method='POST',
    http_conn_id='fastapi_conn',
    endpoint='/monitor',
    dag=dag,
)

retrain_task = SimpleHttpOperator(
    task_id='retrain_task',
    method='POST',
    http_conn_id='fastapi_conn',
    endpoint='/retrain',
    dag=dag,
)

# Setting the schedule for each task
predict_task.set_upstream(None)  # This will be executed daily
monitor_task.set_upstream(None)  # This will be executed twice a week
retrain_task.set_upstream(None)  # This will be executed twice a month
