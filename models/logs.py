# from flask import jsonify
from pymongo import MongoClient
from pymongo import ASCENDING
import datetime

from books.models import MongoLogObject

# client = MongoClient('mongodb://localhost:27017/')
# db = client.my_logs
# log_collection = db.log
# log_collection.ensure_index([("timestamp", ASCENDING)])

class LoggerObject():
    i = 0
    # def clearlogtxt(self):
    #     f = open('models/bookreviews.log','w')
    #     f.write("")
    #     f.close()

    def logrequest(self, request, response=None):
        entry = MongoLogObject()
        entry.timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        entry.method = request.method
        entry.url = request.url
        # entry['files'] = request.files
        # entry['args'] = request.args
        # entry['form'] = request.form
        print(response)
        entry.response = str(response)
        entry.save()


    def deleteAllLogs(self):
        collection = MongoLogObject()
        collection.drop_collection()
        pass

    def getAllLogs(self):
        query = MongoLogObject.objects[:10]
        logs = []
        for i in query:
            logs.append(i.serialize())
            print(i.serialize())
        return logs

    def getLogCount(self):
        # return (db.log.find().count())
        pass