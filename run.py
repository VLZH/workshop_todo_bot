import os

from dotenv import load_dotenv
from utils import add_fixtures_todos
from bot import TodoBot


def main():
    # dev
    add_fixtures_todos()
    ######
    load_dotenv()
    token = os.environ.get("ACCESS_TOKEN")
    if token:
        bot = TodoBot(token)
        bot.pooling()
    else:
        raise Exception("Hey guy! You must to define ACCESS_TOKEN variable in .env")


if __name__ == "__main__":
    main()
