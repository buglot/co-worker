import enum 
import socket
import json
class TypeCode(enum.Enum):
    UPDATE = 1
    LOAD = 2
    SYSEMCALL = 3
    CONNECTION =4
    DISCONNECTION =5
    PING=6
    UUID=7
class UpdateType(enum.Enum):
        NEW= 1
        DELETE =2
        RENAME = 3
class TypeIgnore(enum.Enum):
    FOLDER ="FOLDER"
    EXTENSION ="EXTENSION"
    FILENAME ="FILENAME"

class Mysocket():
    __nameClient :str
    uuid:str
    mysocket :socket.socket
    def __init__(self,s :socket.socket) -> None:
        super().__init__()
        self.mysocket = s
    def setName(self,s:str):
        self.__nameClient = s
    def getName(self)->str:
        return self.__nameClient
    def send(self,data:bytes):
        self.mysocket.sendall(data)
    def senddict(self,data:dict,Type:TypeCode):
        data["type"] = Type.value
        data_bytes = json.dumps(data).encode()
        self.mysocket.sendall(data_bytes)

    def close(self):
        self.mysocket.close()

