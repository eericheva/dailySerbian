# coding=utf-8
import asyncio

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
async def get_start_command(message):
    if CURRENT_USER(message) not in MY_USERS(0):
        await telegram_bot_start_session.start_me(message)


@dailySerbian_bot.message_handler(
    commands=[basemodel_dailySerbian.BaseCommand.help.value]
)
async def get_help_command(message):
    await telegram_bot_start_session.start_me(message)


@dailySerbian_bot.message_handler(
    commands=[basemodel_dailySerbian.SpamItems.start_spam.value]
)
async def get_start_spam_command(message):
    base_dict_utils.update_new_spam_flag(
        message, basemodel_dailySerbian.SpamItems.start_spam.value
    )
    await telegram_bot_spam.spam_me(message)


@dailySerbian_bot.message_handler(
    commands=[basemodel_dailySerbian.SpamItems.stop_spam.value]
)
async def get_stop_spam_command(message):
    base_dict_utils.update_new_spam_flag(
        message, basemodel_dailySerbian.SpamItems.stop_spam.value
    )
    await telegram_bot_spam.stop_spam_message(message)


@dailySerbian_bot.message_handler(content_types=["text"])
async def get_messages_text(message):
    global INRUS, INSERB
    INRUS = message.text
    INSERB = await telegram_bot_answers.translate_and_replay_in_text_me(message, INRUS)
    await telegram_bot_answers.voice_me(message, INSERB)
    if len(INRUS) < MAX_STR_LEN_TO_SAVE_DICT:
        await telegram_bot_answers.ask_add2dict(message, INRUS)


@dailySerbian_bot.message_handler(content_types=["document"])
async def get_messages_document(message):
    if message.document.file_size > 500:
        await dailySerbian_bot.send_message(
            CURRENT_USER_ID(message), "NOT PROCEEDED: file is to big!"
        )
        return None
    file_info = await dailySerbian_bot.get_file(message.document.file_id)
    file_path = await dailySerbian_bot.download_file(file_info.file_path)

    global INRUS, INSERB
    INRUS = file_path.decode("utf8")
    INSERB = await telegram_bot_answers.translate_and_replay_in_text_me(message, INRUS)
    await telegram_bot_answers.voice_me(message, INSERB)
    if len(INRUS) < MAX_STR_LEN_TO_SAVE_DICT:
        await telegram_bot_answers.ask_add2dict(message, INRUS)


@dailySerbian_bot.message_handler(content_types=["audio", "voice"])
async def get_messages_voice(message):
    if message.voice.duration > 30:
        await dailySerbian_bot.send_message(
            CURRENT_USER_ID(message), "NOT PROCEEDED: message is to long!"
        )
        return None
    file_info = await dailySerbian_bot.get_file(message.voice.file_id)
    file_path = await dailySerbian_bot.download_file(file_info.file_path)

    global INRUS, INSERB
    INRUS = speech2text_me.speech2text_me(file_path)
    INSERB = await telegram_bot_answers.translate_and_replay_in_text_me(message, INRUS)
    await telegram_bot_answers.voice_me(message, INSERB)
    if len(INRUS) < MAX_STR_LEN_TO_SAVE_DICT:
        await telegram_bot_answers.ask_add2dict(message, INRUS)


@dailySerbian_bot.message_handler(content_types=["photo"])
async def get_messages_photo(message):
    if message.photo[0].file_size > 1024:
        await dailySerbian_bot.send_message(
            CURRENT_USER_ID(message), "NOT PROCEEDED: image is to big!"
        )
        return None
    file_info = await dailySerbian_bot.get_file(message.photo[2].file_id)
    file_path = await dailySerbian_bot.download_file(file_info.file_path)

    global INRUS, INSERB
    inrus_dict_w_coords = image2text_me.image2text_me(file_path)
    INSERB, INRUS = await telegram_bot_answers.translate_and_replay_in_image_me(
        message, inrus_dict_w_coords, file_path
    )
    await telegram_bot_answers.voice_me(message, INSERB)
    if len(INRUS) < MAX_STR_LEN_TO_SAVE_DICT:
        await telegram_bot_answers.ask_add2dict(message, INRUS)


@dailySerbian_bot.callback_query_handler(
    func=lambda call: call.data
    in [basemodel_dailySerbian.Add2dictItems.add2dict_item_yes.value]
)
async def check_button_ask_add2dict_yes(call):
    base_dict_utils.add_new_item_to_this_user_dict(call, INRUS, INSERB)
    await dailySerbian_bot.send_message(CURRENT_USER_ID(call), "ALL COOL! I'm done!")
    await telegram_bot_answers.ask_add2spam(call)


@dailySerbian_bot.callback_query_handler(
    func=lambda call: call.data
    in [basemodel_dailySerbian.Add2dictItems.add2dict_item_no.value]
)
async def check_button_ask_add2dict_no(call):
    await dailySerbian_bot.send_message(
        CURRENT_USER_ID(call), "It's ok, it's ok, shame on you!"
    )


@dailySerbian_bot.callback_query_handler(
    func=lambda call: call.data in [basemodel_dailySerbian.SpamItems.start_spam.value]
)
async def check_button_ask_spam_yes(call):
    await get_start_spam_command(call)


@dailySerbian_bot.callback_query_handler(
    func=lambda call: call.data in [basemodel_dailySerbian.SpamItems.stop_spam.value]
)
async def check_button_ask_spam_no(call):
    await get_stop_spam_command(call)


for this_user in MY_USERS(0):
    base_dict_utils.update_new_spam_flag(
        this_user, basemodel_dailySerbian.SpamItems.stop_spam.value
    )

asyncio.run(dailySerbian_bot.infinity_polling())
