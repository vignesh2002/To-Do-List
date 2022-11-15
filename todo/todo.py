"""This module contains the To-Do Model-Controller"""
# todo/todo.py

from pathlib import Path
from typing import Any, Dict, List, NamedTuple

from todo import DB_READ_ERROR, ID_ERROR
from todo.database import DatabaseHandler

class CurrentTodo(NamedTuple):                                                          # subclass of typing.NamedTuple
    todo: Dict[str, Any]                                                                # subclssing allows us to create named tuples with type hints for named fields.
    error: int

class Todoer:                                                                           # this class using 'composition', so it has a DatabaseHandler component to directly communicate with the to-do database
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)

    def get_todo_list(self) -> List[Dict[str, Any]]:                                    # .get_todo_list() first gets the entire to-do list from the database by calling .read_todos() on the database handler. The call .read_todos() returns a named tuple, DBResponse containing the to-do list and return code. To retrieve only the list, .get_todo_list() returns the .todo_list field only
        """Return the current To-Do List"""
        read = self._db_handler.read_todos()
        return read.todo_list

    def add(self, description: List[str], priority: int = 2) -> CurrentTodo:            # defines .add(), which takes description and priority as arguments. The description is a list of strings. Typer builds this list from the words entered by the user at the command line to describe the current to-do. In the case of priority, it’s an integer value representing the to-do’s priority. The default is 2, indicating a medium priority.
        """Adding a new to-do item to the database"""
        description_text = " ".join(description)                                        # .join() function is used for concatenating description components into single string.
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

    def set_done(self, todo_id: int) -> CurrentTodo:                                    # defines .set_done(). The method takes an argument called todo_id, which holds an integer representing the ID of the to-do to be marked as done.
        """Set a to-do as done"""
        read = self._db_handler.read_todos()                                            # reads all the to-dos by calling .read_todos() on the database handler
        if(read.error):                                                                 # checks if any error occurs during the reading
            return CurrentTodo({}, read.error)                                          # returns a named tuple, CurrentTodo, with an empty to-do and the error
        try:                                                                            # try...except block to catch invalid to-do IDs that translate to invalid indices in the list.
            todo = read.todo_list[todo_id - 1]
        except IndexError:
            return CurrentTodo({}, ID_ERROR)                                            # returns a CurrentTodo instance with an empty to-do and the corresponding error code
        todo["Done"] = True                                                             # assigns True to the "Done" key in the target to-do dictionary
        write = self._db_handler.write_todos(read.todo_list)                            # writes the update back to the database by calling .write_todos() on the database handler
        return CurrentTodo(todo, write.error)                                           # returns a CurrentTodo instance with the target to-do and a return code indicating how the operation went

    def set_undone(self, todo_id: int) -> CurrentTodo:                                  # defines .set_undone(). The method takes an argument called todo_id, which holds an integer representing the ID of the to-do to be marked as undone.
        """Set a to-do as done"""
        read = self._db_handler.read_todos()                                            # reads all the to-dos by calling .read_todos() on the database handler
        if(read.error):                                                                 # checks if any error occurs during the reading
            return CurrentTodo({}, read.error)                                          # returns a named tuple, CurrentTodo, with an empty to-do and the error
        try:                                                                            # try...except block to catch invalid to-do IDs that translate to invalid indices in the list.
            todo = read.todo_list[todo_id - 1]
        except IndexError:
            return CurrentTodo({}, ID_ERROR)                                            # returns a CurrentTodo instance with an empty to-do and the corresponding error code
        todo["Done"] = False                                                            # assigns False to the "Done" key in the target to-do dictionary
        write = self._db_handler.write_todos(read.todo_list)                            # writes the update back to the database by calling .write_todos() on the database handler
        return CurrentTodo(todo, write.error)                                           # returns a CurrentTodo instance with the target to-do and a return code indicating how the operation went

    def remove(self, todo_id: int) -> CurrentTodo:                                      # defines .remove(). This method takes a to-do ID as an argument and removes the corresponding to-do from the database
        """Remove a To-Do from the database using its id of index"""
        read = self._db_handler.read_todos()                                            # reads the to-do list
        if read.error:                                                                  # checks if any error occurs during the reading process
            return CurrentTodo({}, read.error)
        try:                                                                            # try...except block to catch invalid ID input from user
            todo = read.todo_list.pop(todo_id - 1)                                      # removes the to-do at index todo_id - 1 from the to-do list
        except IndexError:
            return CurrentTodo({}, ID_ERROR)
        write = self._db_handler.write_todos(read.todo_list)                            # writes the updated to-do list back to the database
        return CurrentTodo(todo, write.error)                                           # returns a CurrentTodo tuple holding the removed to-do and a return code indicating a successful operation

    def remove_all(self) -> CurrentTodo:                                                # removes all the to-dos from the database by replacing the current to-do list with an empty list
        """Clear entire list of to-dos"""
        write = self._db_handler.write_todos([])
        return CurrentTodo({}, write.error)                                             # For consistency, the method returns a CurrentTodo tuple with an empty dictionary and an appropriate return or error code