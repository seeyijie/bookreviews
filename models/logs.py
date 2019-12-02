# from flask import jsonify
from pymongo import MongoClient
from pymongo import ASCENDING
import datetime

from models.MongoLogObject import MongoLogObject


# client = MongoClient('mongodb://localhost:27017/')
# db = client.my_logs
# log_collection = db.log
# log_collection.ensure_index([("timestamp", ASCENDING)])

class LoggerObject():
    i = 0

    def logrequest(self, request, response=None):
        entry = MongoLogObject()
        entry.timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        entry.method = request.method
        entry.url = request.url
        entry.response = str(response)
        entry.save()

    def deleteAllLogs(self):
        collection = MongoLogObject()
        collection.drop_collection()
        pass

    def getAllLogs(self):
        query = MongoLogObject.objects.order_by('-timestamp').limit(10)
        logs = []
        for i in query:
            logs.append(i.serialize())
            # print(i.serialize())
        return logs

    def getLogCount(self):
        # return (db.log.find().count())
        pass