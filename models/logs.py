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

    def logrequest(self, request):
        entry = {}
        entry['method'] = request.method
        entry['url'] = request.url
        entry['files'] = request.files
        entry['args'] = request.args
        entry['form'] = request.form
        log_collection.insert(entry)

    def deleteAllLogs(self):
        log_collection.remove()

    def getAllLogs(self):
        return list(log_collection.find())
    
    def getLogCount(self):
        return (db.log.find().count())

if __name__ == "__main__":
    print(log.getAllLogs())