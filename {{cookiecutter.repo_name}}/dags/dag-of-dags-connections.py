import os
from datetime import datetime
from airflow import DAG, settings
from airflow.models import Connection
from airflow.operators.python_operator import PythonOperator
from airflow.operators.http_operator import SimpleHttpOperator
from airflow.sensors.http_sensor import HttpSensor


def create_dag(dag_id, schedule, dag_number, default_args):
    def hello_world_py(*args, **kwargs):
        print("Hello World")
        print("This is DAG: {}".format(str(dag_number)))

    dag = DAG(dag_id, schedule_interval=schedule, default_args=default_args)

    with dag:
        t1 = PythonOperator(
            task_id="hello_world", python_callable=hello_world_py, dag_number=dag_number
        )

        sensor = HttpSensor(
            task_id='check_server_online',
            http_conn_id=dag_id,
            endpoint='',
            request_params={},
            response_check=lambda response: "httpbin" in response.text,
            poke_interval=5,
            dag=dag,
        )

        t2 = SimpleHttpOperator(
            task_id=dag_id,
            method='GET',
            http_conn_id=dag_id,
            endpoint='',
            data={"q": "ousmane conde"},
            headers={},
            dag=dag,
        )

        t1 >> sensor
        t1 >> t2

    return dag


session = settings.Session()

conns = (
    session.query(Connection.conn_id)
        .filter(Connection.conn_id.ilike("%crawl%"))
        .all()
)

for conn in conns:
    dag_id = "{}".format(conn[0])

    default_args = {
        'owner': os.environ["DAG_OWNER"],
        'start_date': datetime.now(),
        'depends_on_past': False,
        'email': ['ouc642@g.harvard.edu'],
        'email_on_failure': False,
        'email_on_retry': False,
        # 'retries': 0,
        # 'retry_delay': timedelta(minutes=5),
        'provide_context': True
    }

    schedule = "@once"

    dag_number = conn

    globals()[dag_id] = create_dag(dag_id, schedule, dag_number, default_args)
