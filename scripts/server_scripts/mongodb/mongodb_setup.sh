#!/bin/bash

# dropbox url is the first command line argument
dropbox_url=$1

echo "Installing MongoDB"
wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | sudo apt-key add -

# use this for ubuntu 18.04
echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/4.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.2.list

sudo apt-get -y update
sudo apt-get install libcurl3 -y
sudo apt-get install -y mongodb-org=4.2.0 mongodb-org-server=4.2.0 mongodb-org-shell=4.2.0 mongodb-org-mongos=4.2.0 mongodb-org-tools=4.2.0
echo "done installing MongoDB"

sudo systemctl start mongod
sudo systemctl enable mongod

echo "Importing dataset to MongoDB"
sudo mongoimport --db 50043_db --collection books_metadata --file /home/ubuntu/data_store/meta_Kindle_Store.json --legacy

echo "Downloading bookreviews repository"
# wget -c https://www.dropbox.com/s/6g4zfii8f0d7yny/bookreviews.zip?dl=0 -O bookreviews.zip
wget -c $dropbox_url -O bookreviews.zip
sudo apt-get install -y unzip

echo "Unzipping bookzreview.zip"
unzip bookreviews.zip -d "/home/ubuntu/bookreviews"

