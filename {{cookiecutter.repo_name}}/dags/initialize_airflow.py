import os
import logging
from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator
from airflow import settings
from airflow.models import Connection
from airflow.api.common.experimental.pool import create_pool

log = logging.getLogger(__name__)

default_args = {
    'owner': os.environ["DAG_OWNER"],
    'start_date': datetime.now(),
    'depends_on_past': False,
    'retries': 0,
    'provide_context': True
}

dag = DAG('initialize_environment',
          default_args=default_args,
          schedule_interval='@once',
          catchup=False,
          dagrun_timeout=timedelta(seconds=30)
          )


# create connections
def create_connections():
    session = settings.Session()  # get the session
    slack_conn = Connection(
        conn_id='slack_token_id',
        login=os.environ['DEFAULT_SLACK_CHANNEL'],
        password=os.environ['SLACK_BOT_TOKEN'],
    )  # create a connection object

    session.add(slack_conn)
    session.commit()  # it will insert the connection object programmatically in airflow


# create pools
def create_pools():
    create_pool("default_pool", 128, "default pool for tasks")
    create_pool("large_pool", 1024, "large pool to handle tasks parallelism surgically")


create_connections = PythonOperator(
    task_id='create_connections',
    provide_context=False,
    python_callable=create_connections,
    dag=dag)

create_pools = PythonOperator(
    task_id='create_pools',
    provide_context=False,
    python_callable=create_pools,
    dag=dag)

create_pools >> create_connections
