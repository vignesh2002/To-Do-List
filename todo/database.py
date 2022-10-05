"""This Module provides Database functionality to the application"""
# todo/database.py

import configparser
from pathlib import Path

from todo import DB_WRITE_ERROR, SUCCESS

DEFAULT_DB_FILE_PATH = Path.home().joinpath(                # define DEFAULT_DB_FILE_PATH to hold the default database file path. The application will use this path if the user doesn’t provide a custom one.
    "." + Path.home().stem + "_todo.json"
)

def get_database_path(config_file: Path) -> Path:           # define get_database_path()
    """Return the current path to the to-do database"""
    config_parser = configparser.ConfigParser()             # this function takes the path to the app’s config file as an argument and
    config_parser.read(config_file)                         # reads the input file using ConfigParser.read() and 
    return Path(config_parser["General"]["database"])       # returns a Path object representing the path to the to-do database on your file system. The ConfigParser instance stores the data in a dictionary. The "General" key represents the file section that stores the required information. The "database" key retrieves the database path. 

def init_database(db_path: Path) -> int:                    # define init_database()
    """Creating the database"""                             # this function takes a database path and writes a string representing an empty list.
    try:
        db_path.write_text("[]")                            # calls the write_text() on the database path, and the list initializes the JSON database with an empty to-do list
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR