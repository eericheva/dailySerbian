import os
from gtts import gTTS

from utils.setup import CURRENT_USER_ID, USER_DICT_PATH


def text2speech_me(message, inserb):
    # todo https://www.codingem.com/best-ai-voice-generators/
    voice = gTTS(text=inserb, lang="sr", slow=False)
    voice_file = os.path.join(USER_DICT_PATH, str(CURRENT_USER_ID(message)) + ".ogg")
    voice.save(voice_file)
    voice = open(voice_file, "rb")
    return voice
