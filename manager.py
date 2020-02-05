import uuid
from typing import List, Optional


class ManagerException(Exception):
    pass


class TodosManager:
    """
    Keep list of todos and provide methods for working with them
    """

    default: Optional["TodosManager"] = None

    def __init__(self):
        self.todos = list()  # type: List['Todo']

    def add_todo(self, todo: "Todo"):
        "Add todo item to list"
        self.todos.append(todo)

    def remove_todo(self, todo_id: str):
        "Remove todo from managery by id"
        todo = self._get_item_by_id(todo_id)
        del self.todos[self.todos.index(todo)]

    def toggle_todo(self, todo_id: str):
        "Change todo status by id"
        todo = self._get_item_by_id(todo_id)
        todo.toggle()

    def _get_item_by_id(self, todo_id: str) -> "Todo":
        for todo in self.todos:
            if todo.id == todo_id:
                return todo
        raise ManagerException("Todo not found")


TodosManager.default = TodosManager()


class Todo:
    """
    Todo item with text information and completed status
    """

    def __init__(self, text):
        self.id = uuid.uuid4().hex  # type: str
        self.text = text  # type: str
        self.completed = False  # type: bool

    def __str__(self):
        return f"{self.text}{'✅' if self.completed else '✖️'}"

    def toggle(self):
        "Change status"
        self.completed = not self.completed
