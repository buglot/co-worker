from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import socket
import time
from watchdog.observers import Observer
import threading
import os
import socket
import uuid 
import typing
import json
from TypeCode import TypeCode,Mysocket
import Checksum
import Ignore
from Mywatchdog import NewFileHandler

Clients : typing.Dict[typing.Any,Mysocket] = {}
Folder_look : str
def Type4do(UUID):
    socket=Clients[UUID]
    Ignorefile = Ignore.IgnoreFile()
    data = {}
    if os.path.exists(".ckignore"):
        data={"ignore": Ignorefile.data}
    lists = []
    for root,directory,files in os.walk(Folder_look):
        for x in directory:
            if not Ignorefile.Folder_Check(os.path.join(x)):
                directory.remove(x)
                print("del :",x,directory)
        for file in files:
            if Ignorefile.Check(a:=os.path.join(root,file)):
                print("add",a)
                lists.append(a)
    data["sha256"] =  Checksum.allChacksum(lists,Folder_look)
    data["portFTP"]=4931
    data["connect"]=[]
    for x in Clients.keys():
        data["connect"].append([x[:8],Clients[x].getName()])
        if x!=UUID:
            Clients[x].senddict({"user":[UUID[:8],Clients[UUID].getName()]},TypeCode.CONNECTION)
    print(data)
    socket.senddict(data,TypeCode.LOAD)
def TypeChecker(data:str):
    _newData :dict=json.loads(data)
    UUID = _newData["UUID"]
    match TypeCode(_newData["type"]):
        case TypeCode.CONNECTION:
            Clients[UUID].setName(_newData["name"])
            do_threading = threading.Thread(target=Type4do,args=[UUID],daemon=True,name="do findong file")
            do_threading.start()
        case TypeCode.PING:
            socket=Clients[UUID]
            socket.senddict({},TypeCode.PING)
def handle_client(client_socket : Mysocket, client_address):
    print(f"Accepted connection from {client_address}")
    while True:
        try:
            request = client_socket.mysocket.recv(16384)
            if not request:
                break
            TypeChecker(request.decode())
        except ConnectionResetError:
            print(f"Connection with {client_address} was reset.")
            break
        except Exception as e:
            print(f"Error handling client {client_address}: {e}")
            break
    client_socket.close()
    print(f"Closed connection from {client_address}")
    uuidclient = client_socket.uuid
    Clients.pop(client_socket.uuid)
    for x in Clients.keys():
        Clients[x].senddict({"UUID":uuidclient},Type=TypeCode.DISCONNECTION)
def start_server(port=3322):
    global Clients
    host = get_ip_addresses()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"[*] Listening on {host}:{port}")
    while True:
        client_socket, client_address = server.accept()
        uuidClient = str(uuid.uuid4())
        mysocket = Mysocket(client_socket)
        mysocket.uuid = uuidClient
        Clients[uuidClient] = mysocket
        client_handler = threading.Thread(target=handle_client, args=(mysocket, client_address),daemon=True)
        
        data={"type":TypeCode.UUID.value,"UUID":uuidClient}
        Clients[uuidClient].send(json.dumps(data).encode())
        client_handler.start()

def get_ip_addresses():
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)
def run_ftp_server(folder:str):
    authorizer = DummyAuthorizer()
    authorizer.add_user("user", "12345", folder, perm="elradfmwMT")  # เปลี่ยนเส้นทางและข้อมูลผู้ใช้ตามต้องการ
    handler = FTPHandler
    handler.authorizer = authorizer
    ipserver = get_ip_addresses()
    port = 4931
    server = FTPServer((ipserver, port), handler)  # กำหนด IP และพอร์ต
    server.serve_forever()


def start_watchdog(path):
    print("Now pid Watchdog",os.getpid())
    try:
        event_handler = NewFileHandler()
        observer = Observer()
        observer.schedule(event_handler, path, recursive=True)
        observer.start()
        print(f"Started watching directory: {path}")
        while True:
            time.sleep(1)
    except Exception as e:
        print(f"Error in start_watchdog: {e}")
        observer.stop()
    observer.join()


def ThreadingProgram():
    global Folder_look
    Folder_look = input("Folder (c:/program) : ")
    ftp_thread = threading.Thread(target=run_ftp_server,args=[os.path.join(Folder_look),])
    socket_thread = threading.Thread(target=start_server,daemon=True)
    start_watchdog_thread = threading.Thread(target=start_watchdog,args=[os.path.join(Folder_look),])
    start_watchdog_thread.daemon = True
    ftp_thread.daemon = True
    start_watchdog_thread.start()
    ftp_thread.start()
    socket_thread.start()
    while 1:
        pass

if __name__ == "__main__":
    ThreadingProgram()
