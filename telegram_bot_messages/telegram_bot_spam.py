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
        inserb = "\n".join(base_inserb[this_index])
        result = "******** Time to train some words ******** \n"
        result += f"{inrus} \n --> \n {inserb}\n"
        result += (
            f" ---- If you do not want to receive train spam, \n "
            f"just send me {basemodel_dailySerbian.SpamItems.stop_spam.value} --- "
        )
        dailySerbian_bot.send_message(
            CURRENT_USER_ID(message), result, time.sleep(3600)
        )


def start_spam_message(message):
    dailySerbian_bot.send_message(
        CURRENT_USER_ID(message),
        f"Hooray, you have got turned on spam "
        f"I will send you some phrases from you dictionary in the nearest future. \n"
        f"If you change you mind, just send me "
        f"/{basemodel_dailySerbian.SpamItems.stop_spam.value}",
    )


def stop_spam_message(message):
    dailySerbian_bot.send_message(
        CURRENT_USER_ID(message),
        f"It's ok, it's ok, you have got turned off spam. "
        f"Shame on you! "
        f"If you change you mind, just send me "
        f"/{basemodel_dailySerbian.SpamItems.start_spam.value}",
    )
