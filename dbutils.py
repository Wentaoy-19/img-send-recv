import dropbox

from pymongo import MongoClient
import pymongo
from datetime import datetime
import time
import os 

class cloudStorage:
    def __init__(self,token) -> None:
        self.token = token
        self.dbx = dropbox.Dropbox(token)
    def upload(self,fromPath, toPath):
        self.dbx = dropbox.Dropbox(self.token)
        with open(fromPath,'rb') as fp:
            tmp = fp.read()
            try:
                retval = self.dbx.files_upload(tmp,toPath)
                print(retval)
                return 0
            except:
                print("ERROR UPLOAD")
                return -1
    def download(self, toPath, fromPath):
        try:
            me, res = self.dbx.files_download(fromPath)
        except:
            print("ERROR DOWNLOAD")
            return -1
        with open(toPath + f"/{me.name}",'wb') as fpout:
            fpout.write(res.content)
        return toPath + f"/{me.name}"
    def delete(self,path):
        try:
            _ = self.dbx.files_delete(path)
            return 0
        except:
            return -1

class mongoDB:
    def __init__(self,connstr):
        self.client = MongoClient(connstr)
        self.db = self.client['bridgedb']
        self.collections = self.db['expbeam']
    def insert(self,imgpath, camid):
        pkg = {
            "time": datetime.now(),
            "imgpath": imgpath,
            "camid": camid,
            "is_read": False        
        }
        self.collections.insert_one(pkg)
    def findall(self):
        ret = []
        c = self.collections.find({"is_read":False})
        for item in c:
            ret.append(item)
        return ret
    def update(self,query,val):
        self.collections.update_one(query,val)
    def setreadall(self,inlist):
        for item in inlist:
            q = {"_id": item['_id']}
            v = {"$set": {"is_read":True}}
            self.update(q,v)
        return