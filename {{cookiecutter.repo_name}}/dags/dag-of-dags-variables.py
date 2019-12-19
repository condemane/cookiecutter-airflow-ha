import os
from datetime import datetime, timedelta

from airflow import DAG
from airflow.models import Variable

from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator

from airflow.hooks.base_hook import BaseHook
from operators.slack_operator import SlackOperator

# Create JSON Variable if it doesn't exist in the ADMIN
INIT_VARS_DICT = [
    {
        'dag_number': '5',
    },
]

# Get JSON Variable from airflow if created in the admin
INIT_VARS = Variable.get("init_vars",
                         default_var=INIT_VARS_DICT,
                         deserialize_json=True)


def create_dag(dag_id, schedule, dag_number, default_args, catchup=False):
    def print_hello_py(*args, **kwargs):
        print("Hello World")
        print("This is DAG: {}".format(str(dag_number)))

    def print_world(*args, **kwargs):
        print("world")

    dag = DAG(
        dag_id, schedule_interval=schedule, default_args=default_args, catchup=catchup
    )

    with dag:
        hello_world = PythonOperator(
            task_id="hello_world",
            python_callable=print_hello_py,
            dag_number=dag_number,
            pool="default_pool",
        )

        print_hello_in_batch = BashOperator(
            task_id="print_hello_in_batch",
            bash_command='echo "hello"',
            pool="default_pool",
        )
        sleep = BashOperator(
            task_id="sleep", bash_command="sleep 5", pool="default_pool"
        )
        print_world = PythonOperator(
            task_id="print_world", python_callable=print_world, pool="default_pool"
        )

        run_this_last = DummyOperator(task_id="run_this_last")

        notify_user = SlackOperator(
            task_id="notify_user",
            pool="default_pool",
            txt="test msge",
            channel=BaseHook.get_connection("slack").login,
        )

        run_this_first = BashOperator(task_id="run_this_first", bash_command="echo 1")

        # Example of faulty dag with cycle. Don't do things like this.
        # print_hello >> sleep >> print_world

        hello_world >> sleep >> print_world >> print_hello_in_batch >> run_this_last
        notify_user
    return dag


number_of_dags = INIT_VARS[0]['dag_number']
number_of_dags = int(number_of_dags)

for n in range(1, number_of_dags):
    # Dynamically generates dags based on variable provided in the UI
    dag_id = "hello_{}".format(str(n))

    default_args = {
        "owner": os.environ["DAG_OWNER"],
        "start_date": datetime.now(),
        "depends_on_past": False,
        "retries": 3,
        "retry_delay": timedelta(minutes=5),
        "provide_context": True,
        "max_active_runs": 1,
        "email": ["airflow@example.com"],
        "email_on_failure": False,
        "email_on_retry": False,
    }

    # schedule = "@daily"
    schedule = "*/5 * * * *"

    dag_number = n

    globals()[dag_id] = create_dag(dag_id, schedule, dag_number, default_args)
