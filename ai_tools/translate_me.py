from deep_translator import GoogleTranslator, single_detection
from utils.setup import DETECT_LANG_API_KEY

translator_ru_sr = GoogleTranslator(source="ru", target="sr")
translator_sr_ru = GoogleTranslator(source="sr", target="ru")


def translate_me(inrus, inrus_to_lang_check=None):
    inrus_to_lang_check = (
        inrus_to_lang_check if inrus_to_lang_check is not None else inrus
    )
    source_lang = single_detection(inrus_to_lang_check, api_key=DETECT_LANG_API_KEY)
    translator = translator_ru_sr if source_lang in ["ru"] else translator_sr_ru
    inserb = translator.translate(inrus)
    return inserb
