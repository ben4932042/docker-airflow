import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

# default setting
default_args = {
    'owner': 'Data Engineer',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(3),
    'email': ['OWNER_EMAIL'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# dag setting
dag = DAG(
    'example_dag_1',
    default_args=default_args,
    description='Example airflow dag.',
    schedule_interval='10 * * * *')

# define tasks
task1 = BashOperator(
    task_id='task_1_1',
    bash_command='',
    dag=dag)

task2 = BashOperator(
    task_id='task_2_1',
    bash_command='',
    dag=dag)

task3 = BashOperator(
    task_id='task_3_1',
    bash_command='',
    dag=dag)

# set upstream, downstream
task1.set_downstream(task2)
task2.set_downstream(task3)
