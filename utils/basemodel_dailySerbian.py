# generated by datamodel-codegen:
#   filename:  basemodel_dailySerbian.json
#   timestamp: 2023-08-02T15:15:25+00:00

from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Extra


class Word(BaseModel):
    counter: Optional[int] = None
    value: Optional[str] = None
    translation: Optional[List[str]] = None


class Add2dictItems(Enum):
    add2dict_item_yes = "add2dict_item_yes"
    add2dict_item_no = "add2dict_item_no"


class SpamItems(Enum):
    start_spam = "start_spam"
    stop_spam = "stop_spam"


class BaseCommand(Enum):
    start = "start"
    help = "help"


class User(BaseModel):
    id: Optional[int] = None
    username: Optional[str] = None
    want2send: Optional[SpamItems] = None
    user_dict: Optional[List[str]] = None


class DailySerbian(BaseModel):
    class Config:
        extra = Extra.forbid

    user: Optional[User] = None
