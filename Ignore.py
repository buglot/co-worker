import os
import TypeCode
import typing
class IgnoreFile:
    data: typing.Dict[TypeCode.TypeIgnore,list] = {}
    __can :bool =False
    def __init__(self) -> None:
        self.data = {}
        if os.path.exists(file:=".ckignore"):
            self.__can = True
            lines = []
            with open(file,"r") as f:
                lines= f.readlines()
                f.close()
            try:
                for x in lines:
                    x = x.replace("\n","")
                    _f,typeignore= x.split(":")
                    if TypeCode.TypeIgnore(typeignore).name not in self.data.keys():
                        self.data[TypeCode.TypeIgnore(typeignore).name] = []
                    self.data[TypeCode.TypeIgnore(typeignore).name].append(_f)
            except Exception as r:
                print(r)
    def Folder_Check(self,path:str)->bool:
        if self.__can:
            _path = path.split("\\")
            for x in _path:
                try:
                    if x in self.data[TypeCode.TypeIgnore.FOLDER.value]:
                        return False
                except KeyError:
                    pass
        return True
    def Check(self,path:str)->bool:
        if self.__can:
            _path = path.split("\\")
            if not self.Folder_Check(path):
                return False 
                

            try:
                for ex in self.data[TypeCode.TypeIgnore.EXTENSION.value]:
                    if _path[-1].endswith(ex):
                        return False
            except KeyError:
                pass
            try:
                if _path[-1] in self.data[TypeCode.TypeIgnore.FILENAME.value]:
                        return False
            except KeyError:
                pass
        return True
        