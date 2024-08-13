from tkinter import (Tk,Label,Button,Entry,
                    messagebox,Event,DISABLED,
                    ACTIVE,Frame,filedialog,
                    Listbox,Scrollbar,
                    END,LEFT,BOTH,RIGHT,TOP
                    )
import os
import watchdog
import threading
import socket
import time
from TypeCode import TypeCode
import json
import typing
import ftplib
import Checksum
class mainAPP(Tk):
    __ip :str
    __portFTP : int
    __uuid : str
    __pathlook:str
    __who:typing.List[list]
    __whowidget : dict
    __pingf:bool = True
    TKonline :Frame
    def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)

        self.title("Co-worker by buglot")
        self.geometry("700x500")
        self.mainLeft=Frame(self)
        self.mainRight=Frame(self,bg="red")
        self.mainLeft.pack(side = LEFT, fill = BOTH)
        self.mainRight.pack(side = LEFT, fill = BOTH, expand = True)
        self.labelTitle = Label(self.mainLeft,text="CO-WORKER",font=("Arial", 12, "bold"))
        self.labelTitle.grid(columnspan=2,sticky="w")

        label1 = Label(self.mainLeft,text="IP Server :")
        label1.grid(row=1,sticky="w",padx=10,pady=10)
        self.textIP = Entry(self.mainLeft,width=30)
        self.textIP.grid(row=1,column=1,columnspan=2,padx=10,pady=10)
        self.button = Button(self.mainLeft,text="Connect",command=self.connectionServer)
        self.button.grid(row=2,column=1,columnspan=3,sticky="e",padx=10,pady=5)
        self.statusServer = Label(self.mainLeft,text="Status : disconnect")
        self.whenConnect()
        self.widgetFTP()
        self.statusServer.grid(row=2,column=0,columnspan=2,sticky="w",padx=10,pady=5)
        self.labelTitle.bind("<Button-1>", self.Labelclick)
    def Labelclick(self,event :Event):
        messagebox.showinfo("Information", "CO-WORKER BY BUGLOT")
        self.labelTitle.config(fg="blue")
    def setStatus(self,t:str):
        self.statusServer.config(text=t)
    def connectionServer(self):
        try:
            self.setStatus("Status : Connecting...")
            self.__ip = self.textIP.get().split(":")[0]
            self.port = int(self.textIP.get().split(":")[1])
            socket_thread = threading.Thread(target=self.socketConnect,args=[self.__ip,self.port],daemon=True)
            socket_thread.start()
        except IndexError as indexError:
            messagebox.showinfo("Error","Error "+self.textIP.get()+ " noting port ip must be->'1.1.1.1:23'")
            self.setStatus("Status : Error IP")
        except ValueError as V:
            messagebox.showinfo("Error","Error "+self.textIP.get().split(":")[1]+ V.__str__())
            self.setStatus("Status : Error Port")
        except Exception as E:
            print(E)
    def socketConnect(self,ip,port):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.__ip, self.port))
            self.setStatus("Status : Connected!!!")
            self.button.config(state=DISABLED)
            while True:
                    data = self.client_socket.recv(16384)
                    self.TypeChecking(data=data)
        except socket.gaierror:
            self.setStatus("Status : Dosn't fund IP SERVER ")
        except socket.timeout:
            self.setStatus("Status : timeout try again")
        except ConnectionResetError as c:
            self.setStatus("Status : Server close")
            messagebox.showinfo("Error","Error "+ c.__str__())
        except ConnectionAbortedError as r:
            self.setStatus("Status : disconnected Server")
        except ConnectionRefusedError as d:
            self.setStatus("Status : Dosn't fund IP SERVER ")
        self.client_socket.close()
        self.button.config(state=ACTIVE)
        self.buttonName.config(state=ACTIVE)
        self.TKConnect.grid_forget()
        try:
            self.bb.grid_forget()
        except:
            print("hided self.bb")
        self.TKonline.grid_forget()
        self.__pingf = True
    def pingServer(self):
        if not self.__pingf:
            time.sleep(2)
        self.start_time = time.time()
        self.send({"UUID":self.__uuid},TypeCode.PING)
        self.__pingf = False
    def send(self,data:dict,type:TypeCode):
        if self.client_socket:
            data["type"] = TypeCode(type).value
            encode = json.JSONEncoder()
            self.client_socket.sendall(encode.encode(data).encode())
    def TypeChecking(self,data:bytes):
        print(data)
        _newdata:dict =json.loads(data)
        match TypeCode(_newdata["type"]):
            case TypeCode.UUID:
                self.__uuid = _newdata["UUID"]
                self.uuidLabel.config(text="UUID : "+self.__uuid[:24]+"...")
                self.uuidLabel.grid()
                self.TKConnect.grid(row=3,columnspan=2,sticky="w",padx=10,pady=5)
            case TypeCode.LOAD:
                self.__who=_newdata["connect"]
                self.__portFTP= _newdata["portFTP"]
                if "ignore" in _newdata.keys():
                    stringIgnorefile:str=""
                    for x in _newdata["ignore"].keys():
                        for y in _newdata["ignore"][x]:
                            stringIgnorefile+=y+":"+x+"\n"
                    with open(".ckignoretest","w+",encoding="UTF-8") as f:
                        f.write(stringIgnorefile)
                        f.close()
                if "sha256" in _newdata.keys():
                    __newdata:list = _newdata["sha256"]
                    with open("log","w",encoding="UTF-8") as f:
                        f.writelines(list(map(lambda x: f"{x[0]}:{x[1]}\n", __newdata)))
                        f.close()
                self.__pathlook=""
                while messagebox.askokcancel("warning","open Folder co-worker"): 
                    self.__pathlook = filedialog.askdirectory(title="open Folder co-worker")
                    if len(self.__pathlook)<=1:
                       if not messagebox.askokcancel("warning","open Folder co-worker continue?"):
                           break
                    else:
                        break
                
                if len(self.__pathlook)<=1:
                    self.bb = Button(self.mainLeft,text="open folder",command=self.openfolder)
                    self.bb.grid(columnspan=2,padx=10,pady=5,sticky="w")
                else:
                    print(self.__pathlook)
                    self.doHavePath()
            case TypeCode.PING:
                self.pingl.config(text=f"ping : {(time.time()-self.start_time)*1000:.0f} ms.")
                ping_thread =  threading.Thread(target=self.pingServer,daemon=True)
                ping_thread.start()
            case TypeCode.CONNECTION:
                if self.TKonline:
                    self.__whowidget[_newdata["user"][0]] = Label(self.TKonline,text="name : "+_newdata["user"][1]+" uuid : xxx"+_newdata["user"][0][3:])
                    self.__whowidget[_newdata["user"][0]].grid(column=0,columnspan=2,sticky="w",padx=5)
            case TypeCode.DISCONNECTION:
                self.__whowidget[_newdata["UUID"][:8]].grid_forget()
                self.__whowidget.pop(_newdata["UUID"][:8])
    def openfolder(self):
        self.__pathlook = filedialog.askdirectory()
        if self.__pathlook:
            self.doHavePath()
            self.bb.grid_forget()

    def widgetOnline(self):
        self.TKonline = Frame(self.mainLeft)
        self.TKonline.grid(row=5,column=0,columnspan=3,sticky="nw",padx=10,pady=5)
        self.pingl = Label(self.TKonline,text="ping : null")
        self.pingServer()
        self.pingl.grid(row=0,column=0,columnspan=2,sticky="w")
       
        if len(self.__pathlook)>35:
            labelpath = Label(self.TKonline,text="Path:"+self.__pathlook[:35]+"...")
            labelpath.grid(row=1,column=0,columnspan=2,sticky="w")
        else:
            labelpath = Label(self.TKonline,text="Path:"+self.__pathlook)
            labelpath.grid(row=1,column=0,columnspan=2,sticky="w")
        labelwho = Label(self.TKonline,text="Co-Worker Online List")
        labelwho.grid(row=2,column=0,columnspan=2,sticky="w")
        labelwho.config(font=("Arial",10,"bold"))
        self.__whowidget = {}
        for n,x in enumerate(self.__who):
            self.__whowidget[x[0]]=Label(self.TKonline,text="name : "+x[1]+" uuid : xxx"+x[0][3:])
            self.__whowidget[x[0]].grid(column=0,columnspan=2,sticky="w",padx=5)
    def doHavePath(self):
        self.widgetOnline()
        lookfiles_thread = threading.Thread(target=self.lookFilesSameServer,daemon=True)
        lookfiles_thread.start()
        lookfiles_thread.join()
    def lookFilesSameServer(self):
        line:str
        lists=[]
        with open("log","r") as f:
            while 1:
                line = f.readline().rstrip('\n')
                print(line)
                if not line:
                    break
                x,y= line.split(":")
                if not os.path.exists(os.path.join(self.__pathlook,x)):
                    lists.append(os.path.join(x))
                elif os.path.exists(os.path.join(self.__pathlook,x)):
                    if y!=Checksum.calculate_checksum(os.path.join(self.__pathlook,x)):
                        lists.append(os.path.join(x))
            f.close()
        if (t:=len(lists))>0:
            if messagebox.askyesno("Not Founded Files",f"do you want to download {t} files? Do you want to download {t} files? A Files will be similar to the server"):
               ftp_thread = threading.Thread(target=self.connect_ftp_server,daemon=True,args=[lists])
               ftp_thread.start()
            else:
                watchdogThread = threading.Thread(target=self.watchdog,daemon=True)
                watchdogThread.start()
    def connect_ftp_server(self,files:list,watchdog:bool=False,username="user", password="12345"):
            print((self.textIP.get().split(":")[0],self.__portFTP))
            ftp = ftplib.FTP()
            ftp.connect(self.textIP.get().split(":")[0],self.__portFTP)
            # เข้าสู่ระบบ FTP server
            ftp.login(user=username, passwd=password)
            self.setStatusFtp("Status FTP : Online",bg="skyblue")
            # แสดงรายการไฟล์ในไดเรกทอรีปัจจุบัน
            current = ftp.pwd()
            print(current)
            ftp.retrlines('LIST')
            for x in files:
                is_cd = False
                print("dir name: ",os.path.dirname(x))
                if os.path.dirname(x)!="":
                    ftp.cwd(os.path.dirname(x))
                    is_cd = True
                    os.makedirs(os.path.join(self.__pathlook,os.path.dirname(x)), exist_ok=True)
                with open(os.path.join(self.__pathlook,x), 'wb') as file:
                    ftp.retrbinary(f"RETR {os.path.basename(x)}", file.write)
                    self.AddLog(f"Downloaded : {os.path.join(self.__pathlook,x)}")
                if is_cd:
                    ftp.cwd(current)
            # ปิดการเชื่อมต่อ
            ftp.quit()
            self.setStatusFtp("Status FTP : OFFLINE",bg="red")
            if watchdog:
                watchdogThread = threading.Thread(target=self.watchdog,daemon=True)
                watchdogThread.start()

    def widgetFTP(self):
        self.WidgetFTP_Frame = Frame(self.mainRight)
        self.WidgetFTP_Frame.pack(fill=BOTH,expand=True)
        Titlelabel = Label(self.WidgetFTP_Frame,text="FTP Connection",font=("Arial",11,"bold"))
        Titlelabel.pack(side=TOP,fill="x")
        self.lableFtpStatus = Label(self.WidgetFTP_Frame,text="Status FTP : OFFINE",bg="red",fg="white")
        self.lableFtpStatus.pack(side="top")
        self.scoll = Scrollbar(self.WidgetFTP_Frame,orient="vertical")
        self.doingtext = Listbox(self.WidgetFTP_Frame,yscrollcommand = self.scoll.set,width=50)
        self.doingtext.pack(side=LEFT,fill="both",expand=True)
        self.doingtext.bind("<<ListboxSelect>>",self.on_select)
        self.scoll.pack(side=RIGHT,fill="both")
        self.scoll.config( command = self.doingtext.yview )
    def setStatusFtp(self,data:str,bg:str):
        self.lableFtpStatus.config(text=data,bg=bg)
    def AddLog(self,data:str):
        self.doingtext.insert(0, data)
        if self.doingtext.size() >= 100:
            self.doingtext.delete(100)
    def on_select(self,event):
    # Get the selected item(s)
        selected_indices = self.doingtext.curselection()
        if selected_indices:
            selected_item = self.doingtext.get(selected_indices[0])
            messagebox.showinfo("show",f"{selected_item}")
    def whenConnect(self):
        self.TKConnect = Frame(self.mainLeft)
        self.uuidLabel = Label(self.TKConnect ,text="UUID:")
        self.TKConnect.grid_forget()
        self.uuidLabel.grid(row=0,column=0,columnspan=2,sticky="w")
        self.disconnectButton = Button(self.TKConnect,text="disconnect",bg="red",fg="white",command=self.dicconectionButtonClick)
        self.disconnectButton.grid(row=0,column=2,columnspan=3,sticky="e")
        lablename = Label(self.TKConnect,text="Name:")
        lablename.grid(row=1,column=0,columnspan=2,sticky="w")
        self.name = Entry(self.TKConnect,width=25)
        self.name.grid(row=1,column=1,columnspan=2,sticky="e",pady=5)
        self.buttonName = Button(self.TKConnect,text="confirm",command=self.NameButtonClick)
        self.buttonName.grid(row=1,column=3,sticky="e",pady=5)
    def dicconectionButtonClick(self):
        self.client_socket.close()

    def NameButtonClick(self):
        self.buttonName.config(state=DISABLED)
        self.send({"name":self.name.get() if self.name.get()!="" else "unknown","UUID":self.__uuid},TypeCode.CONNECTION)
    def watchdog(self):
        pass
    
app = mainAPP(sync=True)
app.mainloop()