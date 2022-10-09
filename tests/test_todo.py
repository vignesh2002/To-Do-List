# tests/test_todo.py
import json
import pytest
from typer.testing import CliRunner

from todo import (
    DB_READ_ERROR, 
    SUCCESS, 
    __app_name__,
    __version__,
    cli,
    todo,
)

runner = CliRunner()

def test_version():                                                             # defines first unit test for testing application version
    result = runner.invoke(cli.app, ["--version"])                              # calls .invoke() on runner to run the application with the --version option.
    assert result.exit_code == 0                                                # asserts that the application’s exit code (result.exit_code) is equal to 0 to check that the application ran successfully.
    assert f"{__app_name__} v{__version__}\n" in result.stdout                  # asserts that the application’s version is present in the standard output, which is available through result.stdout.

@pytest.fixture                                                                 # pytest fixtures are functions that are used to manage app states and dependencies. They can provide data for testing and a wide range of value types when explicitly called by our testing software. You can use the mock data that fixtures create across multiple tests.
def mock_json_file(tmp_path):                                                   # this fixture creates and returns temporary JSON File - "db_file" with a single to-do list item. The tmp_path is a pathlib.Path object that pytest uses to provide a temporary directory for testing purposes
    todo = [{"Description": "Get milk", "Priority": 2, "Done": False}]
    db_file = tmp_path/"todo.json"
    with db_file.open("w") as db:
        json.dump(todo, db, indent=4)
    return db_file

"""the following two dictonaries provide data to test Todoer.add(). 
The first two keys represent the data you’ll use as arguments to .add(), 
while the third key holds the expected return value of the method."""

test_data1 = {
    "description": ["Clean", "the", "house"],
    "priority": 1,
    "todo": {
        "Description": "Clean the house.",
        "Priority": 1,
        "Done": False,
    },
}
test_data2 = {
    "description": ["Wash the car"],
    "priority": 2,
    "todo": {
        "Description": "Wash the car.",
        "Priority": 2,
        "Done": False,
    },
}

@pytest.mark.parametrize(                                                       # The @pytest.mark.parametrize() decorator marks test_add() for parametrization. When pytest runs this test, it calls test_add() two times. Each call uses one of the parameter sets test_data1, test_data2
    "description, priority, expected",                                          # holds descriptive names for the two required parameters and also a descriptive return value name. The test_add() has the same parameters
    [
        pytest.param(
            test_data1["description"],
            test_data1["priority"],
            (test_data1["todo"], SUCCESS),
        ),
        pytest.param(
            test_data2["description"],
            test_data2["priority"],
            (test_data2["todo"], SUCCESS),
        ),
    ],
)
def test_add(mock_json_file, description, priority, expected):                  # this functions first parameter has the same name as the fixture defined
    todoer = todo.Todoer(mock_json_file)                                        # creates an instance of Todoer with mock_json_file as an argument
    assert todoer.add(description, priority) == expected                        # asserts that a call to .add() using description and priority as arguments should return expected
    read = todoer._db_handler.read_todos()                                      # reads the to-do list from the temporary database and stores it in read variable
    assert len(read.todo_list) == 2                                             # asserts that the length of the to-do list is 2 because mock_json_file() returns a list with one item, and now the test_add() adds a second item to the list.