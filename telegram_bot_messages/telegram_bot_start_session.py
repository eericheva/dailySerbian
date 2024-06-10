from telegram_bot_messages import telegram_bot_answers
from users import base_dict_utils
from utils.setup import CURRENT_USER_ID, dailySerbian_bot


async def start_me(message):
    await dailySerbian_bot.send_message(
        CURRENT_USER_ID(message), "Hello there, new user."
    )
    base_dict_utils.create_new_user(message)
    await dailySerbian_bot.send_message(
        CURRENT_USER_ID(message), "That is what you should know about me:"
    )
    await start_me2(message)
    await dailySerbian_bot.send_message(
        CURRENT_USER_ID(message),
        "Also i can make for you separate dictionary "
        "and spam on you some translations from there from time to time. ",
    )
    await telegram_bot_answers.ask_add2spam(message)


async def start_me2(message):
    await dailySerbian_bot.send_message(
        CURRENT_USER_ID(message),
        "Long story short, I can translate something: texts, documents, voices. "
        "Just send me something in russian or serbian, "
        "and I figure out what I can do with it",
    )
