import airflow
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator

default_args = {
    'owner': 'iago',
    'start_date': datetime(2020, 11, 18),
    'retries': 10,
	'retry_delay': timedelta(hours=1)
}

with airflow.DAG('dag_sparkjob',
                  default_args=default_args,
                  catchup=False,
                  schedule_interval='0 1 * * *') as dag:
    
    bash_sparkjob = BashOperator(
        task_id='saprkjob',
        bash_command="python ${AIRFLOW_HOME}/dags/sparkjob.py",
    )