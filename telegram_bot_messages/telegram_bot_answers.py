import io

import telebot
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

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


async def translate_and_replay_in_text_me(message, inrus):
    inserb = translate_me.translate_me(inrus)
    result = inrus + "\n --> \n" + inserb
    await dailySerbian_bot.send_message(CURRENT_USER_ID(message), result)
    return inserb


async def translate_and_replay_in_image_me(message, inrus, file_path):
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
        inserb = "None" if inserb is None else inserb
        draw.text(xy=coords[0], text=inserb, fill=(0, 0, 0), font=font)
        inserb_out.append(inserb)
    await dailySerbian_bot.send_photo(CURRENT_USER_ID(message), f)
    inrus = inrus_out
    inserb = "\n".join(inserb_out)
    if len(inrus) < MAX_STR_LEN_TO_SAVE_DICT:
        result = inrus + "\n --> \n" + inserb
        await dailySerbian_bot.send_message(CURRENT_USER_ID(message), result)
    return inserb, inrus


async def voice_me(message, inserb):
    voice = text2speech_me.text2speech_me(message, inserb)
    await dailySerbian_bot.send_voice(CURRENT_USER_ID(message), voice)


async def ask_add2dict(message, inrus):
    this_user_inrus_flag = base_dict_utils.check_item_to_this_user_dict(message, inrus)
    if this_user_inrus_flag:
        counter = base_dict_utils.update_item_to_this_user_dict(message, inrus)
        await dailySerbian_bot.send_message(
            CURRENT_USER_ID(message),
            f"You are a little bit forgotten  "
            f"and you have asked about this translation {counter} times already",
        )
        await ask_add2spam(message)
    else:
        item_yes = telebot.types.InlineKeyboardButton(
            text="DO IT!",
            callback_data=basemodel_dailySerbian.Add2dictItems.add2dict_item_yes.value,
        )
        item_no = telebot.types.InlineKeyboardButton(
            text="Just forget about it!",
            callback_data=basemodel_dailySerbian.Add2dictItems.add2dict_item_no.value,
        )
        markup = telebot.types.InlineKeyboardMarkup().add(item_yes, item_no)
        await dailySerbian_bot.send_message(
            CURRENT_USER_ID(message),
            "This is somehow new thing. Should I add this to you dictionary?",
            reply_markup=markup,
        )


async def ask_add2spam(call):
    user_spam_flag = base_dict_utils.check_user_spam_flag(call)
    if user_spam_flag in [
        basemodel_dailySerbian.SpamItems.stop_spam.value,
        False,
        None,
    ]:
        await dailySerbian_bot.send_message(
            CURRENT_USER_ID(call), "You do not receive any spam from me right now."
        )
        item_yes = telebot.types.InlineKeyboardButton(
            text="DO IT!",
            callback_data=basemodel_dailySerbian.SpamItems.start_spam.value,
        )
        item_no = telebot.types.InlineKeyboardButton(
            text="Just forget about it!",
            callback_data=basemodel_dailySerbian.SpamItems.stop_spam.value,
        )
        markup = telebot.types.InlineKeyboardMarkup().add(item_yes, item_no)
        await dailySerbian_bot.send_message(
            CURRENT_USER_ID(call),
            "I should turn on and spam on you, shouldn't I?",
            reply_markup=markup,
        )
