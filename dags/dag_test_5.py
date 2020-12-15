from datetime import datetime, timedelta


from airflow import DAG
# Operators; we need this to operate!
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import BranchPythonOperator, PythonOperator
from airflow.contrib.hooks.redis_hook import RedisHook
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'someone',
    'depends_on_past': False,
    'start_date': datetime(2020, 2, 24),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'end_date': datetime(2020, 2, 29),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
}


dag = DAG(
    dag_id='my_dag',
    description='my dag',
    default_args=default_args,
    schedule_interval='*/1 * * * *'
)


get_timestamp = BashOperator(
    task_id='get_timestamp',
    bash_command='date +%s',
    xcom_push=True,
    dag=dag
)

branching = BranchPythonOperator(
    task_id='branching',
    python_callable=lambda **context: 'store_in_redis' if int(context['task_instance'].xcom_pull(task_ids='get_timestamp')) % 2 == 0 else 'skip',
    provide_context=True,
    dag=dag,
)


def set_last_timestamp_in_redis(**context):
    timestamp = context['task_instance'].xcom_pull(task_ids='get_timestamp')
    redis = RedisHook(redis_conn_id='redis_default').get_conn()
    redis.set('last_timestamp', timestamp)


store_in_redis = PythonOperator(
    task_id='store_in_redis',
    python_callable=set_last_timestamp_in_redis,
    provide_context=True,
    dag=dag
)


skip = DummyOperator(
    task_id='skip',
    dag=dag
)

get_timestamp >> branching >> [store_in_redis, skip]
