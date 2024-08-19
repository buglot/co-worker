from watchdog.events import FileSystemEventHandler,DirMovedEvent,FileMovedEvent
import Ignore
import TypeCode
import socket
import threading
import os
class NewFileHandler(FileSystemEventHandler):
    def __init__(self):
        self.Ignore = Ignore.IgnoreFile()
    def on_created(self, event):
        if self.Ignore.Check(event.src_path) and not os.path.isdir(event.src_path):
            print(f"พบไฟล์ใหม่: {event.src_path}")
            do_new_thread=threading.Thread(target=self.do_new,args=[event.src_path],daemon=True)
            do_new_thread.start()
    def on_modified(self, event):
        if self.Ignore.Check(event.src_path) and not os.path.isdir(event.src_path):
            print(f"ไฟล์ถูกแก้ไข: {event.src_path}")
            domodi_thread = threading.Thread(target=self.do_modi,args=[event.src_path],daemon=True)
            domodi_thread.start()
    def on_deleted(self,event):
        if self.Ignore.Check(event.src_path):
            print(f"ไฟล์ถูกลบ: {event.src_path}")
            # self.do_delete(event.src_path)
    def on_any_event(self,event):
        if type(event) == DirMovedEvent or type(event) == FileMovedEvent:
            print(f"{type(event)}: {event.src_path} {event.dest_path}")
    def do_new(self):
        pass
    def do_modi(self):
        pass
    def do_delete(self):
        pass