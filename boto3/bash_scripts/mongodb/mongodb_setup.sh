#!/bin/bash

dropbox_url=$1

echo "Installing MongoDB"
wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | sudo apt-key add -

# install dependencies for mongodb
echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/4.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.2.list
sudo apt-get -y update
sudo apt-get install libcurl3 -y
sudo apt-get install -y mongodb-org=4.2.0 mongodb-org-server=4.2.0 mongodb-org-shell=4.2.0 mongodb-org-mongos=4.2.0 mongodb-org-tools=4.2.0
echo "done installing MongoDB"

# enable starting of mongodb services when server is powered on
sudo systemctl start mongod
sudo systemctl enable mongod
sudo service mongod start

# downloading of our code repository
echo "Downloading bookreviews repository"
wget -c $dropbox_url -O bookreviews.zip
sudo apt-get install -y unzip

echo "Unzipping bookzreview.zip"
unzip bookreviews.zip -d "/home/ubuntu/bookreviews"

# run script to generate new metadata
echo "Merging new metadata"
sudo apt-get install -y python3-pip # install pip3 for merge_cover_texts.py
yes | pip3 install fire # install dependencies for merge_cover_texts.py
python3 /home/ubuntu/bookreviews/scripts/server_scripts/mongodb/merge_cover_texts.py --meta_json="/home/ubuntu/data_store/meta_Kindle_Store.json" --texts_csv="/home/ubuntu/bookreviews/extra_data/kindle_cover_texts.csv" --output_json="/home/ubuntu/data_store/meta_new.json"

echo "Importing edited dataset to MongoDB"
sudo mongoimport --db 50043_db --collection books_metadata --file /home/ubuntu/data_store/meta_new.json --legacy

echo "Replacing default configuration files"
yes | sudo rm /etc/mongod.conf
sudo mv /home/ubuntu/mongod.conf /etc/
sudo chown root /etc/mongod.conf # give back root permissions to the config file
sudo chmod 644 /etc/mongod.conf

echo "Restarting mongod service"
sudo service mongod restart
sleep 5 # sleep for 5 seconds to make sure service has restarted

echo "creating user for database"
mongo < /home/ubuntu/create_user.js