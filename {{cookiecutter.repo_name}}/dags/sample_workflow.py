import os
from datetime import datetime, timedelta

from airflow import DAG

from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator

from airflow.hooks.base_hook import BaseHook
from operators.slack_operator import SlackOperator


def create_dag(dag_id, schedule, dag_number, default_args, catchup=False):
    def print_hello(*args, **kwargs):
        print("Hello")

    def print_world(*args, **kwargs):
        print("world")

    dag = DAG(
        dag_id, schedule_interval=schedule, default_args=default_args, catchup=catchup
    )

    with dag:
        task_1 = PythonOperator(
            task_id="task1",
            python_callable=print_hello,
            dag_number=dag_number,
            pool="default_pool",
        )

        task_2 = BashOperator(
            task_id="task2",
            bash_command='echo "hello from bash"',
            pool="default_pool",
        )
        task_3 = BashOperator(
            task_id="task_3", bash_command="sleep 5", pool="default_pool"
        )
        task_4 = PythonOperator(
            task_id="task_4", python_callable=print_world, pool="default_pool"
        )

        task_5 = DummyOperator(task_id="task_5")

        task_6 = SlackOperator(
            task_id="task_6",
            pool="default_pool",
            txt="Hi there! this is a slack notification from your dag",
            channel=BaseHook.get_connection("slack_token_id").login,
        )

        task_7 = DummyOperator(task_id="task_7")
        task_8 = DummyOperator(task_id="task_8")
        task_9 = DummyOperator(task_id="task_9")
        task_10 = DummyOperator(task_id="task_10")
        task_11 = DummyOperator(task_id="task_11")

        task_1 >> task_2 >> task_4 >> task_8 >> task_11
        task_1 >> task_3 >> task_5 >> task_9 >> task_11
        task_1 >> task_6 >> task_5 >> task_9 >> task_11
        task_1 >> task_3 >> task_7 >> task_10 >> task_11

    return dag


# Dynamically generates dags based on variable provided in the UI
dag_id = "sample_workflow"
dag_number = dag_id

default_args = {
    "owner": os.environ["DAG_OWNER"],
    "start_date": datetime.now(),
    "depends_on_past": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "provide_context": True,
    "max_active_runs": 1,
    "email": ["ouc642@g.harvard.edu"],
    "email_on_failure": False,
    "email_on_retry": False,
}

# schedule = "@daily"
schedule = "*/5 * * * *"  ## every 5 minutes
globals()[dag_id] = create_dag(dag_id, schedule, dag_number, default_args)
