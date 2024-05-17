from users import base_dict_utils
from telegram_bot_messages import telegram_bot_answers
from utils.setup import CURRENT_USER_ID, dailySerbian_bot


def start_me(message):
    dailySerbian_bot.send_message(CURRENT_USER_ID(message), "Hello there, new user.")
    base_dict_utils.create_new_user(message)
    dailySerbian_bot.send_message(
        CURRENT_USER_ID(message), "That is what you should know about me:"
    )
    start_me2(message)
    dailySerbian_bot.send_message(
        CURRENT_USER_ID(message),
        "Also i cam make for you separate dictionary "
        "and spam on you some translations from there from time to time. ",
    )
    telegram_bot_answers.ask_add2spam(message)


def start_me2(message):
    dailySerbian_bot.send_message(
        CURRENT_USER_ID(message),
        "Long story short, I can translate something: texts, documents, voices. "
        "Just send me something in russian or serbian, "
        "and I figure out what I can do with it",
    )
