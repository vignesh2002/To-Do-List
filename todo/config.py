"""Configuration file to store the file path of the database and other details"""
# todo/config

import configparser                                         # this class allows to handle config files with structures similar to INI files
from pathlib import Path                                    # cross-platform way to handle system paths

import typer            

from todo import (
    DB_WRITE_ERROR, DIR_ERROR, FILE_ERROR, SUCCESS, __app_name__
)

CONFIG_DIR_PATH = Path(typer.get_app_dir(__app_name__))     # holds path of application
CONFIG_FILE_PATH = CONFIG_DIR_PATH/"config.ini"             # holds path of config file

def init_app(db_path: str) -> int:                          # initializes the application's configuration file and database
    """Initialise the application"""
    config_code = _init_config_file()                       # calles the _init_config_file() helper function to create config directory using Path.mkdir(). Also used to create config file using Path.touch().
    if config_code != SUCCESS:
        return config_code
    database_code = _create_database(db_path)               # calls the _create_database() helper function, which creates the to-do database.
    if database_code != SUCCESS:
        return database_code
    return SUCCESS

def _init_config_file() -> int:
    try:
        CONFIG_DIR_PATH.mkdir(exist_ok=True)
    except OSError:
        return DIR_ERROR
    try:
        CONFIG_FILE_PATH.touch(exist_ok=True)
    except OSError:
        return FILE_ERROR
    return SUCCESS

def _create_database(db_path: str) -> int:
    config_parser = configparser.ConfigParser()
    config_parser["General"] = {"database": db_path}
    try:
        with CONFIG_FILE_PATH.open("w") as file:
            config_parser.write(file)
    except OSError:
        return DB_WRITE_ERROR
    return SUCCESS