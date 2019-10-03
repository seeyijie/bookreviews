import pymongo
from pymongo import MongoClient

client = MongoClient('localhost', 27017)

print (client)
db = client.test_database
db = client['test-database']

print (db)