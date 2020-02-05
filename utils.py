from manager import TodosManager, Todo


def add_fixtures_todos():
    for i in range(10):
        TodosManager.default.add_todo(Todo(f"Todo #{i}"))
