from environs import Env
from flask import Flask, render_template, request
import datetime
from pymongo import MongoClient
import pymysql
from pymongo import ASCENDING

import data             # this imports data.py that I created in the same folder

app = Flask(__name__)

# MongoDB
client = MongoClient('mongodb://localhost:27017/')
# Create test database in MongoDB if not created
db = client.test_database
# Create test collection in test_database if not created in MongoDB
collection = db.test_collection
#Setting up environmant variables
env = Env()
env.read_env()
sql_username = env.str("MYSQL_USER", default="root")
sql_password = env.str("MYSQL_PASSWORD", default="password")
# MySQL
host = "localhost"
port = 3306
dbname = "employees"
user = sql_username
password = sql_password

conn = pymysql.connect(host, user=user, passwd=password, db=dbname)



db = client.my_logs
log_collection = db.log
log_collection.ensure_index([("timestamp", ASCENDING)])


def log(msg, requestType):
    """Log `msg` to MongoDB log"""
    entry = {}
    entry['timestamp'] = datetime.datetime.utcnow()
    entry['msg'] = msg
    entry['requestType'] = requestType
    log_collection.insert(entry)



@app.route('/deletelogs', methods = ['DELETE'])
def deletelogs():
    log_collection.remove()
    return 'ok'


@app.route('/getlogs', methods = ['GET'])
def getlogs():
    return str(list(log_collection.find()))

@app.route('/writelogs', methods = ['GET'])
def write_logs():
    log("hello world","GET")
    return 'Hello world'

@app.route('/')
def hello_world():
    return 'Hello world'

@app.route('/index', methods = ['GET'])         # when you GET request the /index page,
def index():                                    # this function will run, and
    return render_template('index.html')        # you will load the index.html file found inside the templates folder

@app.route('/post', methods = ['POST'])         # from index.html, you can send a post request to /post, then this fn happens and post.html is loaded.
def post():
    data.exampleDict[request.form['key']] = request.form['value']   # this adjusts a dictionary found in data.py
    retDict = data.exampleDict
    return render_template('post.html', retDict = retDict)          # loads post.html, and sends a variable called retDict

@app.route('/browse')
def browse():
    arrayOfBooks = data.hardcodedMongo
    # TODO: Instead of hardcoding arrayOfBooks, call a function that retrieves all books from the MongoDB database, and store it in arrayOfBooks.
    # The format of arrayOfBooks is based off the example in prof's github, and can be viewed from data.py
    return render_template('browse.html', arrayOfBooks = arrayOfBooks)

if __name__ == '__main__':
    app.run(debug=True)