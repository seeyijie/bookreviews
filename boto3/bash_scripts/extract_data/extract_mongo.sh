#!/bin/bash
pip3 install -q boto3 fire

# extract data from mysql database and send to s3 bucket
cd "/home/ubuntu/bookreviews/boto3"
mongo 50043_db --eval 'db.books_metadata.find({},{asin:1,price:1,_id:0}).forEach(printjson)' > mongo.txt
sed '1,4d' mongo.txt > mongo_data.json
rm mongo.txt

# transfer to s3 bucket
python3 /home/ubuntu/bookreviews/boto3/upload_data.py --data_file="mongo_data.json"