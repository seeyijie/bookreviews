#!/bin/bash

# to be run from within the server
cd "/home/ubuntu/bookreviews" || exit
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt

# extract data from mysql database and send to s3 bucket
cd "/home/ubuntu/bookreviews/boto3"
mongo 50043_db --eval 'db.books_metadata.find({},{asin:1,price:1,_id:0}).forEach(printjson)' > mongo.txt
sed '1,4d' mongo.txt > mongo_data.json
rm mongo.txt

# transfer to s3 bucket
python3 boto3/upload_data.py --data_file="mongo_data.json"