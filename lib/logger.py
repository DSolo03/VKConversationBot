import time
class Log():
    isDebug=False
    logfilename=f"./logs/{int(time.time())//1000}.log"
    def __write__(self,text):
        with open(self.logfilename,"a+",encoding="utf-8") as logfile:
            logfile.write(f"{text}\n")
    def __init__(self,debug):
        self.isDebug=debug
    def error(self,text):
        self.__write__(f"[ERR] {text}")
    def warn(self,text):
        self.__write__(f"[WRN] {text}")
    def debug(self,text):
        if self.isDebug:
            self.__write__(f"[DBG] {text}")
