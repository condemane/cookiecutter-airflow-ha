import os
from contextlib import contextmanager
from cookiecutter.utils import rmtree
import datetime
from hypothesis import given, settings
from hypothesis.strategies import text
from hypothesis.strategies import lists, characters


# import subprocess


@contextmanager
def bake_in_temp_dir(cookies, *args, **kwargs):
    result = cookies.bake(*args, **kwargs)
    try:
        yield result
    finally:
        rmtree(str(result.project))


@contextmanager
def inside_dir(dirpath):
    """
    Execute code from inside the given directory
    :param dirpath: String, path of the directory the command is being run.
    """
    old_path = os.getcwd()
    try:
        os.chdir(dirpath)
        yield
    finally:
        os.chdir(old_path)


def test_project_tree(cookies):
    result = cookies.bake(extra_context={"project_slug": "test_project"})
    assert result.exit_code == 0
    assert result.exception is None


def test_basic_project_settings(cookies):
    result = cookies.bake(extra_context={"project_name": "test project"})
    assert result.exit_code == 0
    assert result.exception is None


def test_year_compute_in_license_file(cookies):
    with bake_in_temp_dir(cookies) as result:
        license_file_path = result.project.join("LICENSE")
        now = datetime.datetime.now()
        assert str(now.year) in license_file_path.read()


@settings(max_examples=5)
@given(
    lists(
        text(
            min_size=2,
            max_size=10,
            alphabet=characters(blacklist_categories=("Cc", "Cs")),
        )
    )
)
def test_random_strings_with_hypothesis(test_list):
    for st in test_list:
        assert st in test_list
