from pymongo import MongoClient
from pymongo import ASCENDING

client = MongoClient('mongodb://localhost:27017/')
db = client.my_logs
log_collection = db.log
log_collection.ensure_index([("timestamp", ASCENDING)])

class LoggerObject():
    i = 0
    def clearlogtxt(self):
        f = open('models/bookreviews.log','w')
        f.write("")
        f.close()

    def log(self):     
        try:
            f = open('models/bookreviews.log','r')
        except:
            f = open('bookreviews.log','r')
        # self.deleteAllLogs()
        for line in f.readlines()[self.i:]:
            lineArray = line.split(' : ')
            entry = {}
            try:
                entry['time'] = lineArray[0]
                entry['level'] = lineArray[1]
                entry['name'] = lineArray[2]
                entry['threadName'] = lineArray[3]
                entry['message'] = lineArray[4]
                # entry[str(i)] = line
            except:
                print ("An error occurred, check http://127.0.0.1:5000/log or models/bookreviews.log")
                # quit()
            self.i+=1
            log_collection.insert(entry)
        f.close()

    def deleteAllLogs(self):
        log_collection.remove()

    def getAllLogs(self):
        return list(log_collection.find())
    
    def getLogCount(self):
        return (db.log.find().count())

if __name__ == "__main__":
    log = LoggerObject()
    log.deleteAllLogs()
    log.log()
    print(log.getAllLogs())