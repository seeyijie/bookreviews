#!/bin/bash
pip3 install -q boto3 fire

cd "/home/ubuntu/bookreviews/boto3"
# extract data from mysql database and send to s3 bucket
mysql -u root 50043_DB -e 'select asin, reviewText from reviews' --column-names > mysql_data.csv
python3 /home/ubuntu/bookreviews/boto3/upload_data.py --data_file="mysql_data.csv"