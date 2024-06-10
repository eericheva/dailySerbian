import json
import os

from utils import basemodel_dailySerbian
from utils.setup import (
    CURRENT_USER,
    CURRENT_USER_DICT,
    CURRENT_USER_FILE,
    CURRENT_USER_ID,
    CURRENT_USER_USERNAME,
    MY_USERS,
    USER_DICT_PATH,
)


# DICT_ITEM
def add_new_item_to_this_user_dict(message, inrus, inserb):
    new_item = {"counter": 1, "value": inrus, "translation": [inserb]}
    create_new_user(message)
    this_user_dict = CURRENT_USER_DICT(message)
    if len(this_user_dict.get("user").get("user_dict")) > 30:
        base_counter = [l.get("counter") for l in this_user_dict]
        least_counter = min(base_counter)
        least_idx = [i for i, l in base_counter if l == least_counter][0]
        del this_user_dict["user"]["user_dict"][least_idx]
    this_user_dict["user"]["user_dict"].append(new_item)
    json.dump(
        this_user_dict,
        open(os.path.join(USER_DICT_PATH, CURRENT_USER_FILE(message)), "w"),
    )


def update_item_to_this_user_dict(message, inrus):
    create_new_user(message)
    this_user_dict = CURRENT_USER_DICT(message)
    this_user_inrus = this_user_dict.get("user").get("user_dict")
    this_user_inrus = [s for s in this_user_inrus if s.get("value") == inrus][0]
    this_user_inrus["counter"] += 1
    json.dump(
        this_user_dict,
        open(os.path.join(USER_DICT_PATH, CURRENT_USER_FILE(message)), "w"),
    )
    return this_user_inrus["counter"]


def check_item_to_this_user_dict(message, inrus):
    create_new_user(message)
    this_user_dict = CURRENT_USER_DICT(message)
    this_user_inrus = this_user_dict.get("user").get("user_dict")
    this_user_inrus = [s.get("value") for s in this_user_inrus]
    return inrus in this_user_inrus


# SPAM_FLAG
def update_new_spam_flag(message, flag):
    create_new_user(message)
    this_user_dict = CURRENT_USER_DICT(message)
    this_user_dict["user"]["want2send"] = flag
    json.dump(
        this_user_dict,
        open(os.path.join(USER_DICT_PATH, CURRENT_USER_FILE(message)), "w"),
    )


def update_new_spam_time(message, new_time):
    create_new_user(message)
    this_user_dict = CURRENT_USER_DICT(message)
    this_user_dict["user"]["last_spam_time"] = new_time
    json.dump(
        this_user_dict,
        open(os.path.join(USER_DICT_PATH, CURRENT_USER_FILE(message)), "w"),
    )


def check_user_spam_flag(message):
    create_new_user(message)
    this_user_dict = CURRENT_USER_DICT(message)
    return this_user_dict.get("user").get("want2send")


# NEW USER
def create_new_user(message):
    new_user = {
        "user": {
            "id": CURRENT_USER_ID(message),
            "username": CURRENT_USER_USERNAME(message),
            "user_dict": create_new_dict(),
            "want2send": basemodel_dailySerbian.SpamItems.stop_spam.value,
        }
    }
    if CURRENT_USER(message) not in MY_USERS(0):
        json.dump(
            new_user,
            open(os.path.join(USER_DICT_PATH, CURRENT_USER_FILE(message)), "w"),
        )
    return new_user


def create_new_dict():
    new_dict = [
        {
            "counter": 1,
            "value": "Здравствуй",
            "translation": ["Здр'аво", "Ч'ао", " Поштов'ање"],
        },
        {
            "counter": 1,
            "value": "До свидания",
            "translation": ["Zb'ogom", "Doviđ'enja", "Пр'иятно"],
        },
        {"counter": 1, "value": "Извините", "translation": ["Žao mi je", "Изв'ини"]},
        {
            "counter": 1,
            "value": "Как дела? - Хорошо. А как ты?",
            "translation": [
                "Kako si? - Д'обро сам? Како си ти?",
                "Како све? - Д'обро сам? Како све ви?",
            ],
        },
        {
            "counter": 1,
            "value": "Спасибо большое вам. - Не зачто. Пожалуйста",
            "translation": ["Хвала пуна вам. - Nema na čemu! Изв'олите"],
        },
        {"counter": 1, "value": "Правильно", "translation": ["T'ačno"]},
        {"counter": 1, "value": "Не правильно", "translation": ["N'etačno"]},
    ]
    return new_dict
