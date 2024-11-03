from sqlite3 import DatabaseError
import sqlite_utils
import datetime
import sys
import os
root=os.getcwd()
sys.path.append("../lib")
from vk import API

class User():
    id=0
    name=""
    joinDate=""
    leaveDate=""
    lastMessage=""
    lastMessageDate=""
    isMuted="False"
    msgCount=0
    comment=""
    __warns__={}
    __bans__={}
    def __init__(self,id: int):
        self.id=id
        usersTable=sqlite_utils.Database("./users.db")["users"]
        if usersTable.count_where("id = ?",[id])!=0:
            usersFound=usersTable.rows_where("id = ?",[id])
            for user in usersFound:
                userDict=user
                break
            self.name=userDict["name"]
            self.joinDate=userDict["joinDate"]
            self.leaveDate=userDict["leaveDate"]
            self.msgCount=userDict["msgCount"]
            self.isMuted=str(userDict["isMuted"])
            self.comment=userDict["comment"]
            self.lastMessage=userDict["lastMessage"]
            self.lastMessageDate=userDict["lastMessageDate"]
            self.comment=userDict["comment"]
            self.__warns__=eval(userDict["warns"])
            self.__bans__=eval(userDict["bans"])
        else:
            if int(self.id)>0:
                userData=API.users.get(user_ids=self.id)[0]
                self.name=f"{userData['first_name']} {userData['last_name']}"
            else:
                self.name="Пользователь"
            usersTable.upsert({"id":self.id,"name":self.name,"joinDate":self.joinDate,"leaveDate":self.leaveDate,"lastMessage":self.lastMessage,"lastMessageDate":self.lastMessageDate,"msgCount":self.msgCount,"comment":self.comment,"warns":str(self.__warns__),"bans":str(self.__bans__),"isMuted":self.isMuted},pk="id")
    def getWarns(self):
        warns=[]
        for warn in self.__warns__:
            warns.append({"date":warn,"reason":self.__warns__[warn]})
        return warns
    def getBans(self):
        bans=[]
        for ban in self.__bans__:
            ban.append({"date":ban,"reason":self.__bans__[ban]})
        return bans
    def mute(self):
        self.isMuted="True"
    def unmute(self):
        self.isMuted="False"
    def addBan(self,reason):
        now = str(datetime.datetime.now())
        self.__bans__.update({now:{"date":now,"reason":reason}})
    def addWarn(self,reason):
        now = str(datetime.datetime.now())
        self.__warns__.update({now:{"date":now,"reason":reason}})
    def setLastMessage(self,message):
        now = datetime.datetime.now()
        self.lastMessage=message
        self.lastMessageDate=str(now)
    def directaccess(self) -> sqlite_utils.Database:
        usersTable=sqlite_utils.Database("./users.db")
        return usersTable
    def update(self):
        usersTable=sqlite_utils.Database("./users.db")["users"]
        if int(self.id)>0:
            userData=API.users.get(user_ids=self.id)[0]
            self.name=f"{userData['first_name']} {userData['last_name']}"
        else:
            self.name="Пользователь"
        usersTable.upsert({"id":self.id,"name":self.name,"joinDate":self.joinDate,"leaveDate":self.leaveDate,"lastMessage":self.lastMessage,"lastMessageDate":self.lastMessageDate,"msgCount":self.msgCount,"comment":self.comment,"warns":str(self.__warns__),"bans":str(self.__bans__),"isMuted":self.isMuted},pk="id")
    def getData(self,field: str):
        return API.users.get(user_ids=self.id,fields=field)[0][field]
    def __str__(self):
        return self.name
