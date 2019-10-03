from flask import Flask
import datetime
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client.test_database
collection = db.test_collection


@app.route('/')
def hello_world():
    # post = {"author": "Mike",
    #         "text": "My first blog post!",
    #         "tags": ["mongodb", "python", "pymongo"],
    #         "date": datetime.datetime.utcnow()}
    #
    # posts = db.posts
    # post_id = posts.insert_one(post).inserted_id
    #
    # return 'Hello World!\n' + str(post_id)
    return 'Hello world'


if __name__ == '__main__':
    app.run()
