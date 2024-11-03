.import os
import sys
root=os.getcwd()
sys.path.append("../lib")

import asyncio
from asyncio import create_task as mktask
import importlib
import re
from random import randint
import time
import sqlite_utils
import datetime

#/lib packages
from vk import API, APIu
from vk import Longpoll
from vk import newMessage
from storage import Storage
from users import User
from attachments import Attachments
from logger import Log

class Bot:
    async def __send__(chatID,text,replyID:int = 0,stickerID:int = 0,attachments:list = []):
        API.messages.send(
            peer_id=chatID+2000000000,
            message=text,
            reply_to=replyID,
            sticker_id=stickerID,
            attachment=",".join(attachments),
            random_id=randint(-102400,102400)
            )

async def main(chatID:int = 0 ,messageID:int = 0, sender: int = 0,context:int = 0 ,text: str = "",attachments: list = [],stickerID:int = 0,actionType:str = "",actionUser:int = 0):
    #Example of bot service
    #Will execute for every message
    pass