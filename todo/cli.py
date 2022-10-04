"""This module provides the Command-Line Interface for the To-Do Application."""
# todo/cli.py

from typing import Optional

import typer

from todo import __app_name__, __version__

app = typer.Typer()

def _version_callback(value: bool) -> None:
    if(value):
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

@app.callback()  
def main(  #Typer callback
    version: Optional[bool] = typer.Option(  #version of type Optional[bool] i.e. bool or none
        None,               # first arg provides options default value
        "--version",        # command-line name of option
        "-v",               # command-line name of option
        help="Show the application's version and exit.",    #help message for version option
        callback=_version_callback,     # attaches callback function to version option => running option calls function directly
        is_eager=True,      # tells typer that version option has precedence over other options in this application
    )
) -> None:
    return
