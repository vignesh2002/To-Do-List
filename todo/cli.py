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
        prompt="Enter To-Do List database location"                             # the prompt argument displays a prompt asking for a database location. It also allows the user to accept the default path by pressing Enter
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
        
@app.command(name="list")                                                       # define list_all() as a typer command. The name argument sets a custom name for the command which is "list" here. 
def list_all() -> None:                                                         # Note.: list_all() doesnt take any argument or option. It just lists the to-dos.
    """List all To-Dos"""
    todoer = get_todoer()                                                       # gets the Todoer instance
    todo_list = todoer.get_todo_list()                                          # gets the to-do list from the database by calling .get_too_list() on todoer
    if len(todo_list) == 0:                                                     # define a conditional statement to check if there’s at least one to-do in the list. If not, then the if code block prints an error message to the screen and exits the application
        typer.secho(
            "There are no tasks in the to-do list yet",
            fg=typer.colors.RED,
        )
        raise typer.Exit()
    typer.secho(
        "\nTo-Do List:\n",                                                      # prints the header to present the to-do list
        fg=typer.colors.BLUE,
        bold=True,                                                              # makes text BOLD
    )
    columns = (                                                                 # print the required columns to display the to-do list in a tabular format
        "ID. ",
        "| Priority ",
        "| Done ",
        "| Description ",
    )
    headers = "".join(columns)
    typer.secho(headers, fg=typer.colors.BLUE, bold=True)
    typer.secho("-" * len(headers), fg=typer.colors.BLUE)
    for id, todo in enumerate(todo_list, 1):                                    # run a for loop to print every single to-do on its own row with appropriate padding and separators
        desc, priority, done = todo.values()
        typer.secho(
            f"{id}{(len(columns[0]) - len(str(id))) * ' '}"
            f"| ({priority}){(len(columns[1]) - len(str(priority)) - 4) * ' '}"
            f"| {done}{(len(columns[2]) - len(str(done)) - 2) * ' '}"
            f"| {desc}",
            fg=typer.colors.BLUE,
        )
    typer.secho("-" * len(headers) + "\n", fg=typer.colors.BLUE)                # prints a line of dashes with a final line feed character (\n) to visually separate the to-do list from the next command-line prompt

@app.command(name="complete")                                                   # define set_done() as a Typer command with name = "complete"
def set_done(todo_id: int =typer.Argument(...)) -> None:                        # set_done() function takes an argument called todo_id, which defaults to an instance of typer.Argument. This instance will work as a required command-line argument
    """Complete a to-do by setting it as done using corresponding todo_id"""
    todoer = get_todoer()                                                       # gets the todoer instance
    todo, error = todoer.set_done(todo_id)                                      # sets the to-do with the specific todo_id as done by calling .set_done() on todoer
    if error:                                                                   # checks for any error occurs during the process
        typer.secho(
            f'Completing to-do # "{todo_id}" failed with "{ERRORS[error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"""todo # {todo_id}"{todo['Description']}" completed!""",
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
