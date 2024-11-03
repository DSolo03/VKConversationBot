version='1.0.0.0'

import os
import sys
root=os.getcwd()
sys.path.append("lib")
sys.path.append("svc")
sys.path.append("bin")

import asyncio
from asyncio import create_task as mktask
import importlib
import re
from random import randint
import time
import sqlite_utils
import datetime
import string

#/lib packages
from vk import API, APIu
from vk import Longpoll
from vk import newMessage
from storage import Storage
from users import User
from attachments import Attachments
from logger import Log

startTime = time.time()
me=-201340515

Storage=Storage()
Log=Log(True)

commands=[]

class Utils:
    def listValToKey(dictionary: dict, value: str):
        for key in dictionary:
            if value in dictionary[key]:
                return key  

    def forBot(event):
        return bool(event.split(" ")[0].lower().translate(str.maketrans('', '', string.punctuation))==Storage("botName").lower())

    def haveAttachments(event):
        return bool(event["attachments"]) 

def services():
    def mapping(string):
        if not os.path.isdir(f"./svc/{string}"):
            return string[0:-3]
        return ""
    svcs=list(map(mapping,os.listdir("./svc")))
    svcsfr=[]
    for svc in svcs:
        if svc:
            svcsfr.append(svc)
    return svcsfr

def commands():
    def mapping(string):
        if not os.path.isdir(f"./bin/{string}"):
            return string[0:-3]
        return ""
    svcs=list(map(mapping,os.listdir("./bin")))
    svcsfr=[]
    for svc in svcs:
        if svc:
            svcsfr.append(svc)
    return svcsfr

async def handler(chatID:int = 0 ,messageID:int = 0, sender: int = 0,context:int = 0 ,text: str = "",attachments: list = [],stickerID:int = 0,actionType:str = "",actionUser:int = 0):
    parsedMessage=await messageParser(text)
    Log.debug(f"{text.split(' ')[0].lower().translate(str.maketrans('', '', string.punctuation))} {Storage('botName').lower()} {Utils.forBot(text)}")
    Log.debug(f"Пришло сообщение. Имя бота: {Storage('botName')}. Текст: {text}. parsedMessage: {parsedMessage}")
    if sender>0:
        for service in services():
            Log.debug(f"Сервис {service} обработан!")
            
            module=importlib.import_module(service)
            importlib.reload(module)
            await module.main(chatID,messageID,sender,context,text,attachments,stickerID,actionType,actionUser)
        for key in parsedMessage:
            if (key in commands()) and (Utils.forBot(text)) and (sender in Storage("admins")):
                try:
                    module=importlib.import_module(key)
                    importlib.reload(module)
                    await module.main(chatID,messageID,sender,context,text,attachments,stickerID,actionType,actionUser)
                except Exception as e:
                    Log.error(f"Невозможно загрузить команду {key}. {e}")
                break
      
async def messageParser(message: str = ""):
    message=message.replace("\n"," ")
    parsedMessage={}
    commandList=[]
    aliases=Storage("aliases")
    for command in aliases:
        for alias in aliases[command]:
            commandList.append(alias)
    for command in commandList:
        if message.find(command)!=-1:
            temp=message
            for subcommand in commandList:
                if message[message.find(command)+len(command):].find(subcommand)!=-1:
                    message=message[:message.find(command)+len(command)+message[message.find(command)+len(command):].find(subcommand)]
            message=message[message.find(command)+len(command):].strip()
            parsedMessage.update({Utils.listValToKey(aliases,command):message})
            message=temp
    return parsedMessage

def getContext(raw):
    if raw["fwd_messages"]:
        return raw["fwd_messages"][0]["from_id"]  
    elif raw.get("reply_message",None):
        return raw["reply_message"]["from_id"] 
    else:
        if re.search("\[[a-zA-Zа-яА-Я0-9 ]+\|[@a-zA-Zа-яА-Я0-9 ]+\]",raw["text"]):
            return re.search("\[[a-zA-Zа-яА-Я0-9 ]+\|[@a-zA-Zа-яА-Я0-9 ]+\]",raw["text"])[0].split("|")[0][3:]
    return 0

async def main():
    Log.warn(f"{Storage('botName')} запущен!")
    Storage("startTime",time.time())
    for event in Longpoll.listen():
        serverEvent=event
        event=event.message
        if serverEvent.type == newMessage and event.from_id!=me:
            task=mktask(handler(
                chatID=event.peer_id-2000000000,
                messageID=event.conversation_message_id,
                sender=event.from_id,
                context=getContext(event),
                text=event.text,
                attachments=Attachments.attachmentsList(event["attachments"]),
                stickerID=Attachments.findSticker(event["attachments"]),
                actionType=event.get("action",{}).get("type",""),
                actionUser=int(event.get("action",{}).get("member_id",0))
            ))
            await task

asyncio.run(main())

