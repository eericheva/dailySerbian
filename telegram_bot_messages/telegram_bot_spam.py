import random
import time

from users import base_dict_utils
from utils import basemodel_dailySerbian
from utils.setup import CURRENT_USER_DICT, CURRENT_USER_ID, dailySerbian_bot


def spam_me(message):
    start_spam_message(message)
    while (
        base_dict_utils.check_user_spam_flag(message)
        == basemodel_dailySerbian.SpamItems.start_spam.value
    ):
        this_user_dict = CURRENT_USER_DICT(message).get("user").get("user_dict")
        base_inrus, base_inserb = zip(
            *[
                (
                    l.get("counter") * [l.get("value")],
                    l.get("counter") * [l.get("translation")],
                )
                for l in this_user_dict
            ]
        )
        base_inrus = [ll for l in base_inrus for ll in l]
        base_inserb = [ll for l in base_inserb for ll in l]
        this_index = random.choice(range(len(base_inrus)))
        inrus = base_inrus[this_index]
        inserb = base_inserb[this_index]
        result = inrus + "\n --> \n" + "\n".join(inserb)
        dailySerbian_bot.send_message(
            CURRENT_USER_ID(message), result, time.sleep(3600)
        )


def start_spam_message(message):
    dailySerbian_bot.send_message(
        CURRENT_USER_ID(message),
        f"Ай заебись, у тебя включен режим спама. "
        f"Буду присылать тебе фразы из твоего словаря в ближайшее "
        f"время. "
        f"Если передумаешь, пришли мне "
        f"/{basemodel_dailySerbian.SpamItems.stop_spam.value}",
    )


def stop_spam_message(message):
    dailySerbian_bot.send_message(
        CURRENT_USER_ID(message),
        f"Ну и хуй с тобой! У тебя отключен режим спама. "
        f"Оствайся тупым! "
        f"Если передумаешь, пришли мне "
        f"/{basemodel_dailySerbian.SpamItems.start_spam.value}",
    )
