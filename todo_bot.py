import os
import logging
from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
from todo_manager import Todo, TodosManager

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("echo-bot")

HELLO_MESSAGE = """
Хэй! Я TODO-бот🤖!
Вот тебе инструкция:
/addtodo - Чтобы добавить задание
Пример: /addtodo Выпустить кракена
/ls - Получить список заданий добавленных в систему
/rm - Если хотите удалить задание
/done - Чтобы поменять статус задания
"""

UNKNOWN_COMMAND_MESSAGE = """
Чувак, а можно ведь понятно выражаться! Да?😡
"""


def fixtureTodos():
    for i in range(10):
        TodosManager.default.addTodo(Todo(f"Todo #{i}"))


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=HELLO_MESSAGE)


def wtf(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=UNKNOWN_COMMAND_MESSAGE
    )


def addTodo(update, context):
    todo_text = " ".join(context.args)
    new_todo = Todo(todo_text)
    TodosManager.default.addTodo(new_todo)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"""
Todo **"{new_todo}"** successfully added!
""",
        parse_mode="Markdown",
    )


def listTodos(update, context):
    todo_text_list = []
    for idx, todo in enumerate(TodosManager.default.todos):
        todo_text = f"""[**{idx + 1}**] | {str(todo)}"""
        todo_text_list.append(todo_text)
    msg = "\n".join(todo_text_list)
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=msg, parse_mode="Markdown"
    )


def removeTodo(update, context):
    keyboard = map(lambda x: [KeyboardButton(str(x))], TodosManager.default.todos)
    markup = ReplyKeyboardMarkup(keyboard)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Выбери какую тудушку ты хочешь удалить",
        reply_markup=markup,
    )


def doneTodo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="done")


def main():
    # dev
    fixtureTodos()
    ######
    load_dotenv()
    token = os.environ.get("ACCESS_TOKEN")
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher
    # /start
    start_handler = CommandHandler("start", start)
    dispatcher.add_handler(start_handler)
    # /add
    addtodo_handler = CommandHandler("addtodo", addTodo)
    dispatcher.add_handler(addtodo_handler)
    # /ls
    list_handler = CommandHandler("ls", listTodos)
    dispatcher.add_handler(list_handler)
    # /rm
    remove_handler = CommandHandler("rm", removeTodo)
    dispatcher.add_handler(remove_handler)
    # /done
    done_handler = CommandHandler("done", doneTodo)
    dispatcher.add_handler(done_handler)
    # handler for unknown commands
    dispatcher.add_handler(MessageHandler(Filters.command, wtf))

    # start listening updates
    updater.start_polling()


if __name__ == "__main__":
    main()
