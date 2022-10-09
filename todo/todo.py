"""This module contains the To-Do Model-Controller"""
# todo/todo.py

from pathlib import Path
from typing import Any, Dict, NamedTuple

from todo.database import DatabaseHandler

class CurrentTodo(NamedTuple):                              # subclass of typing.NamedTuple
    todo: Dict[str, Any]                                    # subclssing allows us to create named tuples with type hints for named fields.
    error: int

class Todoer:                                               # this class using 'composition', so it has a DatabaseHandler component to directly communicate with the to-do database
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)         
