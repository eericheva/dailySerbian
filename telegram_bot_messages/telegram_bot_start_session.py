from users import base_dict_utils
from utils.setup import *
from telegram_bot_messages import telegram_bot_answers


def start_me(message):
    dailySerbian_bot.send_message(
        CURRENT_USER_ID(message), "Дратути, новый пользователь."
    )
    base_dict_utils.create_new_user(message)
    dailySerbian_bot.send_message(
        CURRENT_USER_ID(message), "Вот что ты должен знать обо мне:"
    )
    start_me2(message)
    dailySerbian_bot.send_message(
        CURRENT_USER_ID(message),
        "Еще я могу создать для тебя отдельный словарь "
        "и спамить оттуда переводами время от времени. ",
    )
    telegram_bot_answers.ask_add2spam(message)


def start_me2(message):
    dailySerbian_bot.send_message(
        CURRENT_USER_ID(message),
        "Карочи, я могу переводить всякое: текст, документы, войсы. "
        "Просто пришли мне что нибудь на русском, "
        "а я подумаю, что с этим можно сделать",
    )
