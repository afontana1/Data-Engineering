from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from airflow.providers.airbyte.sensors.airbyte import AirbyteJobSensor 

with DAG(dag_id='airbyte_dag_example',
         default_args={'owner': 'airflow'},
         schedule_interval='@daily',
         start_date=days_ago(1)
    ) as dag:

    mysql_to_s3 = AirbyteTriggerSyncOperator(
        task_id='mysql_to_s3',
        airbyte_conn_id='airbyte_conn',
        connection_id='ff8917bd-bfd6-4a86-ab07-74acad1825a6',
        asynchronous=True,
    )

    airbyte_sensor = AirbyteJobSensor(
        task_id='airbyte_sensor_mysql',
        airbyte_conn_id='airbyte_conn',
        airbyte_job_id=mysql_to_s3.output
    )



    mysql_to_s3 >> airbyte_sensor