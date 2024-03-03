from dbutils import mongoDB, cloudStorage

from pymongo import MongoClient
import pymongo
from datetime import datetime
import time
import os 
import sys

class sendLoop:
    def __init__(self,frompath, topath,sleeptime = 30) -> None:
        self.dbx = cloudStorage("sl.BwsutUdI8gz9LQCYvn__uO1hpw_rzJ8Fxpw-Pt5_De4JMFQ1tzctV04CBcs6PwwuXxAXlWdK4Aq7OuQOdt7HFFMaLjmThiqb5MlMeRqXwDbv6JSWPzkTaR55BD-yoxDaNJItvMcUXH0c4LWHSBty")
        self.mdb = mongoDB("mongodb+srv://wentaoy19:ywt20010509@cluster0.eb0efzy.mongodb.net/movie-api-db")
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
    dbpath = sys.argv[1]
    localpath = sys.argv[2]
    sendloop = sendLoop(localpath, dbpath,5)
    sendloop.run()    