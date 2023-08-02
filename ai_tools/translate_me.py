from deep_translator import GoogleTranslator
translator = GoogleTranslator(source='ru', target='sr')

def translate_me(inrus):
    inserb = translator.translate(inrus)
    return inserb