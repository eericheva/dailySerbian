from ai_tools import text2speech_me
from ai_tools import translate_me
from users import base_dict_utils
from utils.setup import *


def translate_and_replay_in_text_me(message, inrus):
    inserb = translate_me.translate_me(inrus)
    result = inrus + "\n --> \n" + inserb
    dailySerbian_bot.send_message(CURRENT_USER_ID(message), result)
    return inserb


def voice_me(message, inserb):
    voice = text2speech_me.text2speech_me(message, inserb)
    dailySerbian_bot.send_voice(CURRENT_USER_ID(message), voice)


def ask_add2dict(message, inrus):
    this_user_inrus_flag = base_dict_utils.check_item_to_this_user_dict(message, inrus)
    if this_user_inrus_flag:
        counter = base_dict_utils.update_item_to_this_user_dict(message, inrus)
        dailySerbian_bot.send_message(
            CURRENT_USER_ID(message),
            f"Ты долбоеб " f"и спрашивал об этом переводе уже {counter} раз",
        )
        ask_add2spam(message)
    else:
        item_yes = telebot.types.InlineKeyboardButton(
            text="Ебашь, че уж тут!",
            callback_data=Add2dictItems.add2dict_item_yes.value,
        )
        item_no = telebot.types.InlineKeyboardButton(
            text="Впизду!", callback_data=Add2dictItems.add2dict_item_no.value
        )
        markup = telebot.types.InlineKeyboardMarkup().add(item_yes, item_no)
        dailySerbian_bot.send_message(
            CURRENT_USER_ID(message),
            "Это какая-то новая хуета. Добавить эту фразу в твой словарь?",
            reply_markup=markup,
        )


def ask_add2spam(call):
    user_spam_flag = base_dict_utils.check_user_spam_flag(call)
    if user_spam_flag in [SpamItems.stop_spam.value, False, None]:
        dailySerbian_bot.send_message(
            CURRENT_USER_ID(call), "Сейчас у тебя отключен спам от меня."
        )
        item_yes = telebot.types.InlineKeyboardButton(
            text="Ебашь, че уж тут!", callback_data=SpamItems.start_spam.value
        )
        item_no = telebot.types.InlineKeyboardButton(
            text="Впизду!", callback_data=SpamItems.stop_spam.value
        )
        markup = telebot.types.InlineKeyboardMarkup().add(item_yes, item_no)
        dailySerbian_bot.send_message(
            CURRENT_USER_ID(call), "Включить и спамить или как?", reply_markup=markup
        )
