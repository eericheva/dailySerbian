import telebot

from ai_tools import text2speech_me
from ai_tools import translate_me
from users import base_dict_utils
from utils import basemodel_dailySerbian
from utils.setup import (
    CURRENT_USER_ID,
    dailySerbian_bot,
    font_file,
    MAX_STR_LEN_TO_SAVE_DICT,
)

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import io


def translate_and_replay_in_text_me(message, inrus):
    inserb = translate_me.translate_me(inrus)
    result = inrus + "\n --> \n" + inserb
    dailySerbian_bot.send_message(CURRENT_USER_ID(message), result)
    return inserb


def translate_and_replay_in_image_me(message, inrus, file_path):
    f = Image.open(io.BytesIO(file_path))
    draw = ImageDraw.Draw(f)
    font = ImageFont.truetype(font_file, size=12)
    inrus_out = "\n".join([_inrus[1] for _inrus in inrus])
    inserb_out = []
    for coords, _inrus, _ in inrus:
        inserb = translate_me.translate_me(_inrus, inrus_out)
        draw.rectangle(
            xy=[tuple(coords[0]), tuple(coords[2])], fill=(255, 255, 255), outline="red"
        )
        draw.text(xy=coords[0], text=inserb, fill=(0, 0, 0), font=font)
        inserb_out.append(inserb)
    dailySerbian_bot.send_photo(CURRENT_USER_ID(message), f)
    inrus = inrus_out
    inserb = "\n".join(inserb_out)
    if len(inrus) < MAX_STR_LEN_TO_SAVE_DICT:
        result = inrus + "\n --> \n" + inserb
        dailySerbian_bot.send_message(CURRENT_USER_ID(message), result)
    return inserb, inrus


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
            callback_data=basemodel_dailySerbian.Add2dictItems.add2dict_item_yes.value,
        )
        item_no = telebot.types.InlineKeyboardButton(
            text="Впизду!",
            callback_data=basemodel_dailySerbian.Add2dictItems.add2dict_item_no.value,
        )
        markup = telebot.types.InlineKeyboardMarkup().add(item_yes, item_no)
        dailySerbian_bot.send_message(
            CURRENT_USER_ID(message),
            "Это какая-то новая хуета. Добавить эту фразу в твой словарь?",
            reply_markup=markup,
        )


def ask_add2spam(call):
    user_spam_flag = base_dict_utils.check_user_spam_flag(call)
    if user_spam_flag in [
        basemodel_dailySerbian.SpamItems.stop_spam.value,
        False,
        None,
    ]:
        dailySerbian_bot.send_message(
            CURRENT_USER_ID(call), "Сейчас у тебя отключен спам от меня."
        )
        item_yes = telebot.types.InlineKeyboardButton(
            text="Ебашь, че уж тут!",
            callback_data=basemodel_dailySerbian.SpamItems.start_spam.value,
        )
        item_no = telebot.types.InlineKeyboardButton(
            text="Впизду!",
            callback_data=basemodel_dailySerbian.SpamItems.stop_spam.value,
        )
        markup = telebot.types.InlineKeyboardMarkup().add(item_yes, item_no)
        dailySerbian_bot.send_message(
            CURRENT_USER_ID(call), "Включить и спамить или как?", reply_markup=markup
        )
