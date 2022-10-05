"""This module provides the Command-Line Interface for the To-Do Application"""
# todo/cli.py

from pathlib import Path
from typing import Optional

import typer

from todo import ERRORS, __app_name__, __version__, config, database

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

def _version_callback(value: bool) -> None:
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
