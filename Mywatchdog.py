from watchdog.events import FileSystemEventHandler
import Ignore
import TypeCode
import socket
import os
class NewFileHandler(FileSystemEventHandler):
    def __init__(self):
        self.Ignore = Ignore.IgnoreFile()
    def on_created(self, event):
        if self.Ignore.Check(event.src_path) and not os.path.isdir(event.src_path):
            print(f"พบไฟล์ใหม่: {event.src_path}")
            self.do_new()
    def on_modified(self, event):
        if self.Ignore.Check(event.src_path) and not os.path.isdir(event.src_path):
            print(f"ไฟล์ถูกแก้ไข: {event.src_path}")
            self.do_modi()
    def on_deleted(self,event):
        if self.Ignore.Check(event.src_path):
            print(f"ไฟล์ถูกลบ: {event.src_path}")
            self.do_delete()
    def do_new(self):
        pass
    def do_modi(self):
        pass
    def do_delete(self):
        pass