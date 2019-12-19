from airflow.models import DagBag


def test_import_dags():
    """ Airflow can successfully import dags"""
    dags = DagBag()
    assert len(dags.import_errors) == 0
