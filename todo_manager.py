import uuid


class TodosManager:
    def __init__(self):
        self.todos = list()

    def addTodo(self, todo):
        self.todos.append(todo)

    def removeTodo(self, todo_idx):
        del self.todos[todo_idx]

    def toggleTodo(self, todo_idx):
        self.todos[todo_idx]


TodosManager.default = TodosManager()


class Todo:
    def __init__(self, text):
        self.id = uuid.uuid4().int
        self.text = text
        self.completed = False

    def __str__(self):
        return f"{self.text}{'✅' if self.completed else '✖️'}"

    def toggle(self):
        self.completed = not self.completed
