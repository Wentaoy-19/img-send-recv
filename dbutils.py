import dropbox

from pymongo import MongoClient
import pymongo
from datetime import datetime
import time
import os 

import logging


class logger():
    def __init__(self,path) -> None:
        fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')        
        self.logger = logging.getLogger(path)
        self.logger.setLevel(logging.DEBUG)
        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        sh.setLevel(logging.DEBUG)
        self.logger.addHandler(sh)
    def info(self,msg):
        self.logger.info(msg)
    def error(self,msg):
        self.logger.error(msg)

class cloudStorage:
    def __init__(self,token) -> None:
        self.token = token
        self.dbx = dropbox.Dropbox(token)
        self.logger = logger("cloudstorage")
    def upload(self,fromPath, toPath):
        self.dbx = dropbox.Dropbox(self.token)
        with open(fromPath,'rb') as fp:
            tmp = fp.read()
            try:
                retval = self.dbx.files_upload(tmp,toPath)
                self.logger.info(f"SUCCESSFUL UPLOAD: {fromPath}")
                return 0
            except:
                self.logger.error(f"ERROR IN UPLOAD: {fromPath}")
                return -1
    def download(self, toPath, fromPath):
        try:
            me, res = self.dbx.files_download(fromPath)
            self.logger.error(f"SUCCESSFUL IN DOWNLOAD: {toPath}/{me.name}")
        except:
            self.logger.error(f"ERROR IN DOWNLOAD: {toPath}/{me.name}")
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
    def insert(self,frompath,imgpath, camid):
        pkg = {
            "time": datetime.now(),
            "frompath": frompath,
            "imgpath": imgpath,
            "camid": camid,
            "is_read": False        
        }
        self.collections.insert_one(pkg)
    def InitSendSet(self,sendSet):
        c = self.collections.find({"is_read": True})
        for item in c:
            path = item['frompath']
            name = path.split("/")[-1]
            sendSet.add(name)
        return
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