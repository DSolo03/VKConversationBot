import json

class Storage():
    storage={}
    def __save__(self):
        json.dump(self.storage,open("./storage.json","w",encoding="utf-8"))
    def __load__(self):
        self.storage=json.load(open("./storage.json","r+",encoding="utf-8"))
    def __init__(self,base: dict = {}):
        self.__load__()
    def __call__(self, *args):
        self.__load__()
        if len(args)==2:
            self.storage.update({args[0]:args[1]})
        elif len(args)==1:
            if isinstance(args[0],str):
                return self.storage.get(args[0],None)
            elif isinstance(args[0],dict):
                return self.storage.update(args[0])
        self.__save__()
    def __str__(self):
        return str(self.storage)
