from PIL import Image
import io
import easyocr

ORCREADER = easyocr.Reader(lang_list=["en", "ru"])


def image2text_me(file_path):
    f = Image.open(io.BytesIO(file_path))
    out = ORCREADER.readtext(f)
    return out
