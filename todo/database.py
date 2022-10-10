"""This Module provides Database functionality to the application"""
# todo/database.py

import configparser
import json
from pathlib import Path
from typing import Any, Dict, List, NamedTuple

from todo import DB_READ_ERROR, DB_WRITE_ERROR, JSON_ERROR, SUCCESS

DEFAULT_DB_FILE_PATH = Path.home().joinpath(                                        # define DEFAULT_DB_FILE_PATH to hold the default database file path. The application will use this path if the user doesn’t provide a custom one.
    "." + Path.home().stem + "_todo.json"
)

def get_database_path(config_file: Path) -> Path:                                   # define get_database_path()
    """Return the current path to the to-do database"""
    config_parser = configparser.ConfigParser()                                     # this function takes the path to the app’s config file as an argument and
    config_parser.read(config_file)                                                 # reads the input file using ConfigParser.read() and 
    return Path(config_parser["General"]["database"])                               # returns a Path object representing the path to the to-do database on your file system. The ConfigParser instance stores the data in a dictionary. The "General" key represents the file section that stores the required information. The "database" key retrieves the database path. 

def init_database(db_path: Path) -> int:                                            # define init_database()
    """Creating the database"""                                                     # this function takes a database path and writes a string representing an empty list.
    try:
        db_path.write_text("[]")                                                    # calls the write_text() on the database path, and the list initializes the JSON database with an empty to-do list
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR

class DBResponse(NamedTuple):                                                       # NamedTuple subclass.                               
    todo_list: List[Dict[str, Any]]                                                 # list of dictionaries representing individual to-dos
    error: int                                                                      # integer error return code

class DatabaseHandler:                                                              # defines DatabaseHandler class that allows to read and write data to the to-do database using json module from the standard library
    def __init__(self, db_path: Path) -> None:                                      # class initializer, takes the path of the database on your file system
        self._db_path = db_path

    def read_todos(self) -> DBResponse:                                             # this method reads the to-do list from the database and deserializes it
        try:                                                                        # try...except block to catch errors while opening the database
            with self._db_path.open("r") as db:                                     # opens the database in "r" - read format
                try:                                                                # try...except block to catch errors while loading and deserialising the JSON file content
                    return DBResponse(json.load(db), SUCCESS)                       # returns a DBResponse type instance holding the result of calling json.load() with the to-do database object as an argument. This result consists of a list of dictionaries. Every dictionary represents a to-do. The error field of DBResponse holds SUCCESS to signal that the operation was successful.
                except json.JSONDecodeError:                                        # catches loading errors of JSON file
                    return DBResponse([], DB_READ_ERROR)
        except OSError:                                                             # catches I/O - loading problems with the JSON file
            return DBResponse([], DB_READ_ERROR)

    def write_todos(self, todo_list: List[Dict[str, Any]]) -> DBResponse:           # takes a list of to-do dictionaries and writes them to the database
        try:                                                                        # try...except block to catch errors while opening the database
            with self._db_path.open("w") as db:                                     # opens the database in "w" - write format
                json.dump(todo_list, db, indent=4)                                  # dumps the to-do list as JSON content into the database
            return DBResponse(todo_list, SUCCESS)                                   # returns a DBResponse instance holding the to-do list and the SUCCESS code.
        except OSError:
            return DBResponse(todo_list, DB_WRITE_ERROR)
