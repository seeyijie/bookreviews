from flask import Flask
import datetime
from pymongo import MongoClient
import pymysql
app = Flask(__name__)

# MongoDB
client = MongoClient('mongodb://localhost:27017/')
# Create test database in MongoDB if not created
db = client.test_database
# Create test collection in test_database if not created in MongoDB
collection = db.test_collection

# MySQL
host = "localhost"
port = 3306
dbname = "employees"
user = "yijie"
password = "password"

conn = pymysql.connect(host, user=user, passwd=password, db=dbname)


@app.route('/')
def hello_world():
    return 'Hello world'


if __name__ == '__main__':
    app.run(debug=True)
