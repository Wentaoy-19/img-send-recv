from dbutils import mongoDB, cloudStorage

from pymongo import MongoClient
import pymongo
from datetime import datetime
import time
import os 
import sys

from crackseg import *

class recvLoop:
    def __init__(self, dbxtoken,mdbtoken,cloudpath, savepath,segpath=None, sleeptime = 30) -> None:
        self.cloudpath = cloudpath
        self.savepath = savepath
        self.sleeptime = sleeptime
        self.segpath = segpath
        self.dbx = cloudStorage(dbxtoken)
        self.mdb = mongoDB(mdbtoken)
        return 
    def run(self):
        while(1):
            mdbitems = self.mdb.findall()
            for item in mdbitems:
                path = item['imgpath']
                retpath = self.dbx.download(fromPath=path, toPath=self.savepath)
                if(self.segpath != None):
                    seg_and_save(retpath, self.segpath)                    
            self.mdb.setreadall(mdbitems)
        return 
    

if __name__ == '__main__':
    dbxtoken = sys.argv[1]
    mdbtoken = sys.argv[2]
    dbpath = sys.argv[3]
    localpath = sys.argv[4]
    if(len(sys.argv)>5):
        segpath = sys.argv[6]
    else:
        segpath = None
    recvloop = recvLoop(dbxtoken,mdbtoken,dbpath, localpath,segpath,5)
    recvloop.run()