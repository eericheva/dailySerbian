import glob
import json
import os

import telebot

if not os.path.isfile("telegram_bot_token.py"):
    TOKEN = os.environ.get("TOKEN")
    DETECT_LANG_API_KEY = os.environ.get("DATECT_LANG_API_KEY")
else:
    from telegram_bot_token import TOKEN, DETECT_LANG_API_KEY

DETECT_LANG_API_KEY = DETECT_LANG_API_KEY
TOKEN = TOKEN

dailySerbian_bot = telebot.TeleBot(TOKEN)
dailySerbian_bot.remove_webhook()

this_project_path = os.getcwd()  # os.path.dirname(os.path.abspath(__file__))
JSON_SCHEMA_PATH = os.path.join(this_project_path, "utils/basemodel_dailySerbian.json")
json_datamodel_path = os.path.join(this_project_path, "utils/basemodel_dailySerbian.py")
font_file = os.path.join(this_project_path, "utils/DejaVuSans.ttf")
if not os.path.isfile(json_datamodel_path):
    os.system(
        f"datamodel-codegen  --input {JSON_SCHEMA_PATH} "
        f"--input-file-type jsonschema "
        f"--output {json_datamodel_path}  "
        f"--target-python-version 3.8 --use-default"
    )

USER_DICT_PATH = os.path.join(this_project_path, "data")
if not os.path.isdir(USER_DICT_PATH):
    os.makedirs(USER_DICT_PATH)
my_user_ends = ".usr.json"
my_users_files = [
    s for s in glob.glob(os.path.join(USER_DICT_PATH, "*")) if s.endswith(my_user_ends)
]
MY_USERS = [s.split("/")[-1].split(my_user_ends)[0] for s in my_users_files]

CURRENT_USER_ID = (
    lambda message: message.from_user.id
    if isinstance(message, telebot.types.Message)
    else int(message.split(".")[0])
)
CURRENT_USER_USERNAME = (
    lambda message: message.from_user.username
    if isinstance(message, telebot.types.Message)
    else message.split(".")[1]
)

CURRENT_USER = (
    lambda message: str(CURRENT_USER_ID(message)) + "." + CURRENT_USER_USERNAME(message)
)
CURRENT_USER_FILE = lambda message: CURRENT_USER(message) + my_user_ends
CURRENT_USER_DICT = lambda message: json.load(
    open(os.path.join(USER_DICT_PATH, CURRENT_USER_FILE(message)), "r")
)

MAX_DICT_LEN = 30
MAX_STR_LEN_TO_SAVE_DICT = 30

# dailySerbian_updater = Updater(TOKEN, use_context=True)
# dailySerbian_dispatcher = dailySerbian_updater.dispatcher
