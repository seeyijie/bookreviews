from pymongo import MongoClient
# client = MongoClient('localhost', 27017)

# resources used: https://realpython.com/introduction-to-mongodb-and-python/

# accessing the databases
# dont need to have existing database
# db = client.newname # attribute is the database name that we wish to access from the mongo server

# # collections and documents are akin to tables and rows in SQL databases
# postsCollection = db.posts # collection named 'posts'
# post_data = { "name" : "Doggo2"}
# result = postsCollection.insert_one(post_data) # inserting an entry into the collection
# print(f"One post: {result.inserted_id}")

# inserting many documents into one collection
# new_result = posts.insert_many([post_1, post_2, post_3])

client = pymongo.MongoClient("mongodb://dom:password@3.15.150.240/50043_db") # defaults to port 27017

db = client.50043_db

# print the number of documents in a collection
print db.books_metadata.count()

# shell command to connect into database on server
# mongo -u dom -p password 3.15.150.240/50043_db