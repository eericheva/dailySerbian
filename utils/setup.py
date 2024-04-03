import glob
import json
import os

# import fastapi
import telebot
from telegram.ext import Updater

if not os.path.isfile("telegram_bot_token.py"):
    TOKEN = os.environ.get("TOKEN")
else:
    from telegram_bot_token import TOKEN

dailySerbian_bot = telebot.TeleBot(TOKEN)
dailySerbian_bot.remove_webhook()
# dailySerbian_app = fastapi.FastAPI(docs=None, redoc_url=None)

# Set webhook
# WEBHOOK_HOST = "national-beetle-super.ngrok-free.app"
# WEBHOOK_PORT = 8443  # 443, 80, 88 or 8443 (port need to be 'open')
# WEBHOOK_URL_BASE = "https://{}:{}".format(WEBHOOK_HOST, WEBHOOK_PORT)
# WEBHOOK_URL_PATH = "/{}/".format(TOKEN)

# WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Path to the ssl certificate
# WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Path to the ssl private key

this_project_path = os.getcwd()  # os.path.dirname(os.path.abspath(__file__))
JSON_SCHEMA_PATH = os.path.join(this_project_path, "utils/basemodel_dailySerbian.json")
json_datamodel_path = os.path.join(this_project_path, "utils/basemodel_dailySerbian.py")
if not os.path.isfile(json_datamodel_path):
    os.system(
        f"datamodel-codegen  --input {JSON_SCHEMA_PATH} "
        f"--input-file-type jsonschema "
        f"--output {json_datamodel_path}  "
        f"--target-python-version 3.8 --use-default"
    )

USER_DICT_PATH = os.path.join(this_project_path, "data")
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

dailySerbian_updater = Updater(TOKEN, use_context=True)
dailySerbian_dispatcher = dailySerbian_updater.dispatcher
