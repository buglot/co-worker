import hashlib
import json
import os
def calculate_checksum(file_path, algorithm='md5'):
    hash_func = hashlib.new(algorithm)
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(16384), b""):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def allChacksum(paths : list,root=None)->dict:
    
    data = []
    for path in paths:
        if root:
            data.append([path[len(root)+1:],calculate_checksum(path)])
        else:
            data.append([path,calculate_checksum(path)])
    return data

def save(data:dict):
    a =json.JSONEncoder()
    with open("log","w+",encoding="UTF-8") as f:
        f.write(a.encode(data))
        f.close()
        
lists = []
for root,directrys,files in os.walk(os.path.join("Project")):
    for file in files:
        lists.append(os.path.join(root,file))
        print(os.path.join(root,file))
save(allChacksum(lists))