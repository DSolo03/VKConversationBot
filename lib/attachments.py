import wget
from vk_api.upload import VkUpload
import requests
import ast
import os
import sys

root=os.getcwd()
sys.path.append("../lib")

#/lib packages
from vk import API as vk
from vk import Longpoll
from vk import newMessage
from storage import Storage
from users import User
from logger import Log

uploader=VkUpload(vk)

class Attachments:
    def ownPhoto(attachment):
        if attachment.get('type')=='photo':
            sizes=attachment.get('photo').get('sizes')
            imageurl=str()
            maxsize=int(0)
            for items in sizes:
                if int(items.get('height'))*int(items.get('width'))>maxsize:
                    maxsize=int(items.get('height'))*int(items.get('width'))
                    imageurl=items.get('url')
            files=wget.download(imageurl,bar=None)
            req=requests.post(vk.photos.getMessagesUploadServer().get('upload_url'), files={'photo':open(files,'rb')})  
            req=ast.literal_eval(req.text)
            atta=vk.photos.saveMessagesPhoto(server=req.get('server'),hash=req.get('hash'),photo=req.get('photo'))[0]
            os.remove(files)
            return ('photo'+str(atta.get('owner_id'))+'_'+str(atta.get('id')))
        return None
    
    def ownGraffiti(attachment):
        if attachment.get('type')=='photo':
            sizes=attachment.get('photo').get('sizes')
            imageurl=str()
            maxsize=int(0)
            for items in sizes:
                if int(items.get('height'))*int(items.get('width'))>maxsize:
                    maxsize=int(items.get('height'))*int(items.get('width'))
                    imageurl=items.get('url')
            files=wget.download(imageurl,bar=None)
            req=requests.post(vk.photos.getMessagesUploadServer().get('upload_url'),params={"type":"graffiti"}, files={'photo':open(files,'rb')})  
            req=ast.literal_eval(req.text)
            atta=vk.photos.saveMessagesPhoto(server=req.get('server'),hash=req.get('hash'),photo=req.get('photo'))[0]
            os.remove(files)
            return ('photo'+str(atta.get('owner_id'))+'_'+str(atta.get('id')))
        return None   

    def ownAudio(attachment):
        if attachment.get('type')=='audio':
            return(('audio'+str(attachment.get('audio').get('owner_id'))+'_'+str(attachment.get('audio').get('id'))))
        return None

    def ownSticker(attachment):
        if attachment.get('type')=='sticker':
            return(attachment.get('sticker').get('sticker_id'))
        return None

    def findSticker(attachments):
        for attachment in attachments:
            if Attachments.ownSticker(attachment):
                return Attachments.ownSticker(attachment)
        return 0

    def createSticker(filename):
        return uploader.graffiti(filename,peer_id=201340515,group_id=201340515)

    def attachmentsList(attachments):
        attachmentsList=[]
        for attachment in attachments:
            if attachment.get('type')=='audio':
                attachmentsList.append(Attachments.ownAudio(attachment))
            if attachment.get('type')=='photo':
                attachmentsList.append(Attachments.ownPhoto(attachment))    
        return attachmentsList