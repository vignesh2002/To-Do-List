"""This module provides the Command-Line Interface for the To-Do Application"""
# todo/cli.py

from pathlib import Path
from typing import Optional, List

import typer

from todo import ERRORS, __app_name__, __version__, config, database, todo

app = typer.Typer()

@app.command()                                                                  # define init() as a Typer command using the @app.command() decorator
def init(
    db_path: str = typer.Option(                                                # define a Typer Option instance and assign it as a default value to db_path.
        str(database.DEFAULT_DB_FILE_PATH), 
        "--db-path",                                                            # command-line name of option to be follwed by database path
        "-db",                                                                  # command-line name of option to be follwed by database path
        prompt="Enter To-Do List database location"                             # the prompt argument displays a prompt asking for a database location. It also allows you to accept the default path by pressing Enter
    ),
) -> None:
    """Initialize the to-do database"""
    app_init_error = config.init_app(db_path)                                   # calls init_app() to create the application’s configuration file and to-do database.
    if (app_init_error):                                                        # check if the call to init_app() returns an error
        typer.secho(                                                            # prints the error message
            f'Creating config file failed with "{ERRORS[app_init_error]}"',
            fg=typer.colors.RED,                                                # sets the error message color to red
        )
        raise typer.Exit(1)                                                     # exits the app with a typer.Exit exception and an exit code of 1 to signal that the application terminated with an error.
    db_init_error = database.init_database(Path(db_path))                       # calls init_database() to initialize the database with an empty to-do list.
    if(db_init_error):                                                          # check if the call to init_database() returns an error
        typer.secho(                                                            # prints the error message
            f'Creating database failed with "{ERRORS[db_init_error]}"',
            fg=typer.colors.RED,                                                # sets the error message color to red
        )
        raise typer.Exit(1)                                                     # exits the app with a typer.Exit exception and an exit code of 1 to signal that the application terminated with an error.
    else:                                                                       # Success case of creation
        typer.secho(                                                            # prints success message
            f"The to-do database is {db_path}",
            fg=typer.colors.GREEN                                               # sets the success message color to green
        )

def get_todoer() -> todo.Todoer:
    if config.CONFIG_FILE_PATH.exists():                                        # checks if applications configuration file exists. Path.exists() method used
        db_path = database.get_database_path(config.CONFIG_FILE_PATH)           # if exists the path to the database is retrieved
    else:
        typer.secho(
            'Config file not found. Please run "todo init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    if db_path.exists():                                                        # check if the path to database exists
        return todo.Todoer(db_path)                                             # if exists an instance of Todoer is created with argument as the retrieved path
    else:
        typer.secho(
            'Database not found. Please run "todo init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

@app.command()
def add(                                                                        # defines .add() as a Typer command using the @app.comand() decorator
    description: List[str] = typer.Argument(...),                               # defines description as an argument to add(). This argument holds a list of strings representing a to-do description. To build the argument, typer.Argument is used. When an ellipsis (...) is passed as the first argument to the constructor of Argument, it tells Typer that description is required. The fact that this argument is required means that the user must provide a to-do description at the command line
    priority: int = typer.Option(                                               # defines priority as a Typer option with a default value of 2. The option names are --priority and -p. Priority only accepts three possible values: 1, 2, or 3. To guarantee this condition, min is set to 1 and max is set to 3. This way, Typer automatically validates the user’s input and only accepts numbers within the specified interval.
        2,
        "--priority",
        "-p",
        min=1,
        max=3,
        )
    ) -> None:
    """Add a new to-do with a description"""
    todoer = get_todoer()                                                       # gets a Todoer instance to be used
    todo, error = todoer.add(description, priority)                             # calls .add() on todoer and unpacks the result into todo and error.
    if error:                                                                   # error handling
        typer.secho(
            f'Adding to-do failed with "{ERRORS[error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"""to-do: "{todo['Description']}" was added """
            f"""with priority: {priority}""",
            fg=typer.colors.GREEN,
        )

def _version_callback(value: bool) -> None:                                     # takes boolean argument value. If value is true then function prints the appliaction name and version.
    if(value):
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

@app.callback()  
def main(                                                                       # Typer callback
    version: Optional[bool] = typer.Option(                                     # version option of type Optional[bool] i.e. bool or none
        None,                                                                   # first arg provides options default value which is set to None here
        "--version",                                                            # command-line name of option
        "-v",                                                                   # command-line name of option
        help="Show the application's version and exit.",                        # help message for version option
        callback=_version_callback,                                             # attaches callback function to version option => running option calls function directly
        is_eager=True,                                                          # tells typer that version option has precedence over other options in this application
    )
) -> None:
    return
