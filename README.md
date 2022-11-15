# To-Do-List CLI Application

**To-Do-List** is a command-line interface application built with [Typer](https://typer.tiangolo.com/) to help you manage your to-do list.

## Installation

To run **To-Do-List**, you need to run the following steps:

1. Clone the application's source code to the `/home/user/` directory
```sh
$ git clone https://github.com/vignesh2002/To-Do-List.git
```
2. Create a Python virtual environment and activate it:

```sh
$ cd To-Do-List/
$ python -m venv ./venv
$ source venv/bin/activate
(venv) $
```

3. Install the dependencies:

```sh
(venv) $ python -m pip install -r requirements.txt
```

4. Initialize the application:

```sh
(venv) $ python -m todo init
```

This command asks you to enter the file path to store the application's database. You can also accept the default file path by just pressing Enter.

## Usage

Once you've cloned the source code and run the installation steps, you can run the following command to access the application's usage description:
```sh
(venv) $ python -m todo --help
```

```sh
Usage: to-do [OPTIONS] COMMAND [ARGS]...

Options:
  -v, --version         Show the application's version and exit.
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or
                        customize the installation.

  --help                Show this message and exit.

Commands:
  add          Add a new to-do with a description
  clear        Remove all to-dos
  init         Initialize the to-do database
  list         List all To-Dos
  mark_done    Complete a to-do by setting it as done using corresponding...
  mark_undone  Complete a to-do by setting it as done using corresponding...
  remove       Remove a to-do using its TODO_ID
  search       Search Value in To-Do List
  sort         List sorted To-Do List
```

You can also access the help message for specific commands by typing the command and then `--help`. For example, to display the help content for the `add` command, you can run the following:

```sh
(venv) $ python -m todo add --help
```

```sh
Usage: to-do add [OPTIONS] DESCRIPTION...

  Add a new to-do with a description

Arguments:
  DESCRIPTION...  [required]

Options:
  -p, --priority INTEGER RANGE  [default: 2]
  --help                        Show this message and exit.
```

Calling `--help` on each command provides specific and useful information about how to use the command at hand.

## Features

**To-Do-List** has the following features:

| Command                                                           | Description                                                  |
| ------------------                                                | ------------------------------------------------------------ |
| `init -db <DATABASE_PATH>`                                        | Initializes the application's to-do database. Options: Database Path. Default: /home/user/user_todo.json              |
| `add <DESCRIPTION> --priority <PRIORITY>`                         | Adds a new to-do to the database with a `DESCRIPTION`. Options: Priority (Range 1-3). Default: 2       |
| `list --order <ORDER_OF_LISTING>`                                 | Lists all the to-dos in the database. Options: Oldest to Newest OR Newest to Oldest. Default: Oldest to Newest                       |
| `sort --order <ORDER_OF_SORTING>`                                 | Sort all the to-dos in the database base based on priority. Options: Ascending OR Descending. Default: Ascending                      |
| `search --text <DESCRIPTION> --index <ID> --priority <PRIORITY>`  | Search among all the to-dos in the database. Options: Text, Index, Priority. Default: None                      |
| `mark_done <TODO_ID>`                                             | Marks a to-do done using its `TODO_ID`. Options: None|
| `mark_undone <TODO_ID>`                                           | Marks a to-do undone using its `TODO_ID`. Options: None|
| `remove <TODO_ID> --force`                                        | Removes a to-do from the database using its `TODO_ID`. Options: Force (Removes to-do without interactive user confirmation prompt)      |
| `clear --force`                                                   | Removes all the to-dos by clearing the database.Options: Force (Removes to-do without interactive user confirmation prompt)             |