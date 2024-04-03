# coding=utf-8
# import telebot
# import uvicorn as uvicorn

from ai_tools import speech2text_me
from telegram_bot_messages import telegram_bot_answers, telegram_bot_start_session
from telegram_bot_messages import telegram_bot_spam
from users import base_dict_utils
from utils import basemodel_dailySerbian
from utils.setup import CURRENT_USER, CURRENT_USER_ID, dailySerbian_bot, MY_USERS

# from utils.setup import dailySerbian_app,  WEBHOOK_PORT, \
#     WEBHOOK_SSL_CERT, \
#     WEBHOOK_SSL_PRIV, WEBHOOK_URL_BASE, \
#     WEBHOOK_URL_PATH


@dailySerbian_bot.message_handler(
    commands=[basemodel_dailySerbian.BaseCommand.start.value]
)
def get_start_command(message):
    if CURRENT_USER(message) not in MY_USERS:
        telegram_bot_start_session.start_me(message)


@dailySerbian_bot.message_handler(
    commands=[basemodel_dailySerbian.BaseCommand.help.value]
)
def get_help_command(message):
    telegram_bot_start_session.start_me(message)


@dailySerbian_bot.message_handler(
    commands=[basemodel_dailySerbian.SpamItems.start_spam.value]
)
def get_start_spam_command(message):
    base_dict_utils.update_new_spam_flag(
        message, basemodel_dailySerbian.SpamItems.start_spam.value
    )
    telegram_bot_spam.spam_me(message)


@dailySerbian_bot.message_handler(
    commands=[basemodel_dailySerbian.SpamItems.stop_spam.value]
)
def get_stop_spam_command(message):
    base_dict_utils.update_new_spam_flag(
        message, basemodel_dailySerbian.SpamItems.stop_spam.value
    )
    telegram_bot_spam.stop_spam_message(message)


@dailySerbian_bot.message_handler(content_types=["text"])
def get_messages_text(message):
    global INRUS, INSERB
    INRUS = message.text
    INSERB = telegram_bot_answers.translate_and_replay_in_text_me(message, INRUS)
    telegram_bot_answers.voice_me(message, INSERB)
    if len(INRUS) < 100:
        telegram_bot_answers.ask_add2dict(message, INRUS)


@dailySerbian_bot.message_handler(content_types=["document"])
def get_messages_document(message):
    if message.document.file_size > 500:
        dailySerbian_bot.send_message(
            CURRENT_USER_ID(message), "в рот я ебал такие большие файлы качать!"
        )
        return None
    file_info = dailySerbian_bot.get_file(message.document.file_id)
    file_path = dailySerbian_bot.download_file(file_info.file_path)

    global INRUS, INSERB
    INRUS = file_path.decode("utf8")
    INSERB = telegram_bot_answers.translate_and_replay_in_text_me(message, INRUS)
    telegram_bot_answers.voice_me(message, INSERB)
    if len(INRUS) < 100:
        telegram_bot_answers.ask_add2dict(message, INRUS)


@dailySerbian_bot.message_handler(content_types=["audio", "voice"])
def get_messages_voice(message):
    if message.voice.duration > 30:
        dailySerbian_bot.send_message(
            CURRENT_USER_ID(message), "в рот я ебал такие длинные сообщения слушать!"
        )
        return None
    file_info = dailySerbian_bot.get_file(message.voice.file_id)
    file_path = dailySerbian_bot.download_file(file_info.file_path)

    global INRUS, INSERB
    INRUS = speech2text_me.speech2text_me(file_path)
    INSERB = telegram_bot_answers.translate_and_replay_in_text_me(message, INRUS)
    telegram_bot_answers.voice_me(message, INSERB)
    if len(INRUS) < 100:
        telegram_bot_answers.ask_add2dict(message, INRUS)


@dailySerbian_bot.callback_query_handler(
    func=lambda call: call.data
    in [basemodel_dailySerbian.Add2dictItems.add2dict_item_yes.value]
)
def check_button_ask_add2dict_yes(call):
    base_dict_utils.add_new_item_to_this_user_dict(call, INRUS, INSERB)
    dailySerbian_bot.send_message(CURRENT_USER_ID(call), "Ай заебись! Я сделаль!")
    telegram_bot_answers.ask_add2spam(call)


@dailySerbian_bot.callback_query_handler(
    func=lambda call: call.data
    in [basemodel_dailySerbian.Add2dictItems.add2dict_item_no.value]
)
def check_button_ask_add2dict_no(call):
    dailySerbian_bot.send_message(
        CURRENT_USER_ID(call), "Ну и хуй с тобой! Оствайся тупым!"
    )


@dailySerbian_bot.callback_query_handler(
    func=lambda call: call.data in [basemodel_dailySerbian.SpamItems.start_spam.value]
)
def check_button_ask_spam_yes(call):
    get_start_spam_command(call)


@dailySerbian_bot.callback_query_handler(
    func=lambda call: call.data in [basemodel_dailySerbian.SpamItems.stop_spam.value]
)
def check_button_ask_spam_no(call):
    get_stop_spam_command(call)


################################################################################################################
# # fastapi
# @dailySerbian_app.post(WEBHOOK_URL_PATH)
# def process_webhook(update: dict):
#     """
#     Process webhook calls
#     """
#     if update:
#         update = telebot.types.Update.de_json(update)
#         dailySerbian_bot.process_new_updates([update])
#     else:
#         return
#
#
# dailySerbian_bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
#                              certificate=open(WEBHOOK_SSL_CERT, 'r')
#                              )
# print(dailySerbian_bot.get_webhook_info())
#
# uvicorn.run(
#         dailySerbian_app,
#         host='0.0.0.0',
#         port=WEBHOOK_PORT,
#         # ssl_certfile=WEBHOOK_SSL_CERT,
#         # ssl_keyfile=WEBHOOK_SSL_PRIV
#         )

################################################################################################################

################################################################################################################
# dailySerbian_bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)
# print(dailySerbian_bot.get_webhook_info())
#
# dailySerbian_bot.run_webhooks(listen="127.0.0.1",
#                               port=443,
#                               # url_path=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,  # WEBHOOK_URL_BASE + WEBHOOK_URL_PATH
#                               # webhook_url=WEBHOOK_URL_BASE,  # WEBHOOK_URL_BASE + WEBHOOK_URL_PATH
#                               # secret_token=NGROK_TOKEN
#                               )
################################################################################################################


dailySerbian_bot.infinity_polling(timeout=20, long_polling_timeout=20)
