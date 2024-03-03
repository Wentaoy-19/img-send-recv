from dbutils import mongoDB, cloudStorage

from pymongo import MongoClient
import pymongo
from datetime import datetime
import time
import os 
import sys

class sendLoop:
    def __init__(self,dbxtoken,mdbtoken,frompath, topath,sleeptime = 30) -> None:
        self.dbx = cloudStorage(dbxtoken)
        self.mdb = mongoDB(mdbtoken)
        self.frompath = frompath
        self.topath = topath
        self.isSent = set()
        self.sleeptime = sleeptime
        return 
    def run(self):
        while(1):
            filelist = os.listdir(self.frompath)
            for file in filelist:
                if(file not in self.isSent):
                    ret = self.dbx.upload(fromPath=f"{self.frompath}/{file}", toPath=f"{self.topath}/{file}")
                    if(ret == 0):
                        # Need to figure out Camera id here
                        self.mdb.insert(imgpath=f"{self.topath}/{file}", camid=0)
                        self.isSent.add(file)
            time.sleep(self.sleeptime)
        return
    

if __name__ == '__main__':
    dbxtoken = sys.argv[1]
    mdbtoken = sys.argv[2]
    dbpath = sys.argv[3]
    localpath = sys.argv[4]
    sendloop = sendLoop(dbxtoken,mdbtoken,localpath, dbpath,5)
    sendloop.run()    