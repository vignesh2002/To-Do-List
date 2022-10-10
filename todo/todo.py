"""This module contains the To-Do Model-Controller"""
# todo/todo.py

from pathlib import Path
from typing import Any, Dict, List, NamedTuple

from todo import DB_READ_ERROR
from todo.database import DatabaseHandler

class CurrentTodo(NamedTuple):                                                          # subclass of typing.NamedTuple
    todo: Dict[str, Any]                                                                # subclssing allows us to create named tuples with type hints for named fields.
    error: int

class Todoer:                                                                           # this class using 'composition', so it has a DatabaseHandler component to directly communicate with the to-do database
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)

    def add(self, description: List[str], priority: int = 2) -> CurrentTodo:            # defines .add(), which takes description and priority as arguments. The description is a list of strings. Typer builds this list from the words entered by the user at the command line to describe the current to-do. In the case of priority, it’s an integer value representing the to-do’s priority. The default is 2, indicating a medium priority.
        """Adding a new to-do item to the database"""
        description_text = " ".join(description)                                        # .join() function is used for
        if not description_text.endswith("."):                                          # adds a "." add the end of a descriptor if the user doesn't to maintain uniformity.
            description_text += "."
        todo = {                                                                        # build a new to-do item based on the user input
            "Description": description_text,
            "Priority": priority,
            "Done": False,
        }
        read = self._db_handler.read_todos()                                            # reads the to-do list from the database by calling the .read_todos() on the database handler.
        if read.error == DB_READ_ERROR:                                                 # checks if .read_todos() returned a DB_READ_ERROR. If so, then returns a named tuple, CurrentTodo, containing the current to-do and the error code.
            return CurrentTodo(todo, read.error)
        read.todo_list.append(todo)                                                     # appends the new to-do to the list.
        write = self._db_handler.write_todos(read.todo_list)                            # writes the updated to-do list to the database by calling .write_todos() on the database handler
        return CurrentTodo(todo, write.error)                                           # returns an instance of CurrentTodo with the current to-do and an appropriate return code.