# coding=utf-8

from ai_tools import image2text_me, speech2text_me
from telegram_bot_messages import telegram_bot_answers, telegram_bot_start_session
from telegram_bot_messages import telegram_bot_spam
from users import base_dict_utils
from utils import basemodel_dailySerbian
from utils.setup import (
    CURRENT_USER,
    CURRENT_USER_ID,
    dailySerbian_bot,
    MAX_STR_LEN_TO_SAVE_DICT,
    MY_USERS,
)


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
    if len(INRUS) < MAX_STR_LEN_TO_SAVE_DICT:
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
    if len(INRUS) < MAX_STR_LEN_TO_SAVE_DICT:
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
    if len(INRUS) < MAX_STR_LEN_TO_SAVE_DICT:
        telegram_bot_answers.ask_add2dict(message, INRUS)


@dailySerbian_bot.message_handler(content_types=["photo"])
def get_messages_photo(message):
    if message.photo[0].file_size > 1024:
        dailySerbian_bot.send_message(
            CURRENT_USER_ID(message), "в рот я ебал такие большие фото обрабатывать!"
        )
        return None
    file_info = dailySerbian_bot.get_file(message.photo[2].file_id)
    file_path = dailySerbian_bot.download_file(file_info.file_path)

    global INRUS, INSERB
    inrus_dict_w_coords = image2text_me.image2text_me(file_path)
    INSERB, INRUS = telegram_bot_answers.translate_and_replay_in_image_me(
        message, inrus_dict_w_coords, file_path
    )
    telegram_bot_answers.voice_me(message, INSERB)
    if len(INRUS) < MAX_STR_LEN_TO_SAVE_DICT:
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


dailySerbian_bot.infinity_polling(timeout=20, long_polling_timeout=20)
