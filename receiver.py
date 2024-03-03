from dbutils import mongoDB, cloudStorage

from pymongo import MongoClient
import pymongo
from datetime import datetime
import time
import os 
import sys

from crackseg import *

class recvLoop:
    def __init__(self, cloudpath, savepath,segpath=None, sleeptime = 30) -> None:
        self.cloudpath = cloudpath
        self.savepath = savepath
        self.sleeptime = sleeptime
        self.segpath = segpath
        self.dbx = cloudStorage("sl.BwsutUdI8gz9LQCYvn__uO1hpw_rzJ8Fxpw-Pt5_De4JMFQ1tzctV04CBcs6PwwuXxAXlWdK4Aq7OuQOdt7HFFMaLjmThiqb5MlMeRqXwDbv6JSWPzkTaR55BD-yoxDaNJItvMcUXH0c4LWHSBty")
        self.mdb = mongoDB("mongodb+srv://wentaoy19:ywt20010509@cluster0.eb0efzy.mongodb.net/movie-api-db")
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
    dbpath = sys.argv[1]
    localpath = sys.argv[2]
    if(len(sys.argv)>3):
        segpath = sys.argv[3]
    else:
        segpath = None
    recvloop = recvLoop(dbpath, localpath,segpath,5)
    recvloop.run()