import logging
import re

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import (
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
    CallbackQueryHandler,
    CallbackContext,
)

from manager import Todo, TodosManager

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

REMOVE_BY_ID_RE = re.compile(r"^%remove\s(?P<todo_id>.+)$")


class TodoBot:
    def __init__(self, token: str):
        self.updater = Updater(token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self._register_handlers()

    def pooling(self):
        self.updater.start_polling()

    def _register_handlers(self):
        # /start
        start_handler = CommandHandler("start", self._start)
        self.dispatcher.add_handler(start_handler)
        # /add
        addtodo_handler = CommandHandler("addtodo", self._addTodo)
        self.dispatcher.add_handler(addtodo_handler)
        # /ls
        list_handler = CommandHandler("ls", self._listTodos)
        self.dispatcher.add_handler(list_handler)
        # /rm
        remove_handler = CommandHandler("rm", self._removeTodo)
        self.dispatcher.add_handler(remove_handler)
        # /rm callback query
        remove_by_id_handler = CallbackQueryHandler(
            self._removeTodoById, pattern=REMOVE_BY_ID_RE
        )
        self.dispatcher.add_handler(remove_by_id_handler)
        # /done
        done_handler = CommandHandler("done", self._doneTodo)
        self.dispatcher.add_handler(done_handler)
        # handler for unknown commands
        self.dispatcher.add_handler(MessageHandler(Filters.command, self._wtf))

    def _start(self, update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.effective_chat.id, text=HELLO_MESSAGE)

    def _wtf(self, update: Update, context: CallbackContext):
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=UNKNOWN_COMMAND_MESSAGE
        )

    def _addTodo(self, update: Update, context: CallbackContext):
        todo_text = " ".join(context.args)
        new_todo = Todo(todo_text)
        TodosManager.default.add_todo(new_todo)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"""
    Todo **"{new_todo}"** successfully added!
    """,
            parse_mode="Markdown",
        )

    def _listTodos(self, update: Update, context: CallbackContext):
        todo_text_list = []
        for idx, todo in enumerate(TodosManager.default.todos):
            todo_text = f"""*[{idx + 1}]* {str(todo)}"""
            todo_text_list.append(todo_text)
        msg = "\n".join(todo_text_list)
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=msg, parse_mode="Markdown"
        )
        print()

    def _removeTodo(self, update: Update, context: CallbackContext):
        keyboard = map(
            lambda x: [InlineKeyboardButton(str(x), callback_data=f"%remove {x.id}")],
            TodosManager.default.todos,
        )
        markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Выбери какую тудушку ты хочешь удалить",
            reply_markup=markup,
            reply_to_message_id=update.message.message_id,
        )

    def _removeTodoById(self, update: Update, context: CallbackContext):
        if TodosManager.default:
            # Получаем ID тудушки из update.callback_query.data
            match = REMOVE_BY_ID_RE.search(update.callback_query.data)
            if match:
                todo_id = match.group("todo_id")
                logger.info(f"Удаление todo по id: {todo_id}")
                #
                TodosManager.default.remove_todo(todo_id)
                context.bot.deleteMessage(
                    chat_id=update.effective_chat.id,
                    message_id=update.callback_query.message.message_id,
                )
                context.bot.sendMessage(
                    chat_id=update.effective_chat.id, text="Задание удалено!🎉"
                )

    def _doneTodo(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="done")
