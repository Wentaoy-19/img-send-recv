from dbutils import mongoDB, cloudStorage

from pymongo import MongoClient
import pymongo
from datetime import datetime
import time
import os 
import sys

class sendLoop:
    def __init__(self,camid,dbxtoken,mdbtoken,frompath, topath,sleeptime = 30) -> None:
        self.dbx = cloudStorage(dbxtoken)
        self.mdb = mongoDB(mdbtoken)
        self.camid = camid
        self.frompath = frompath
        self.topath = topath
        self.isSent = set()
        self.sleeptime = sleeptime
        self.mdb.InitSendSet(self.isSent)
        return 
    def run(self):
        while(1):
            filelist = os.listdir(self.frompath)
            for file in filelist:
                if(file not in self.isSent and file.split(".")[-1]=="jpg"):
                    ret = self.dbx.upload(fromPath=f"{self.frompath}/{file}", toPath=f"{self.topath}/{self.camid}_{file}")
                    if(ret == 0):
                        # Need to figure out Camera id here
                        self.mdb.insert(frompath=f"{self.frompath}/{file}" ,imgpath=f"{self.topath}/{self.camid}_{file}", camid=self.camid)
                        self.isSent.add(file)
            time.sleep(self.sleeptime)
        return
    

if __name__ == '__main__':
    camid = int(sys.argv[1])
    dbxtoken = sys.argv[2]
    mdbtoken = sys.argv[3]
    dbpath = sys.argv[4]
    localpath = sys.argv[5]
    sendloop = sendLoop(camid,dbxtoken,mdbtoken,localpath, dbpath,5)
    sendloop.run()    