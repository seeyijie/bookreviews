#!/bin/bash

# installing mongodb
wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | sudo apt-key add -

# install dependencies for mongodb # does this echo line have issues?
echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/4.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.2.list
apt-get -y update
apt-get install libcurl3 -y
apt-get install -y mongodb-org=4.2.0 mongodb-org-server=4.2.0 mongodb-org-shell=4.2.0 mongodb-org-mongos=4.2.0 mongodb-org-tools=4.2.0

# enable starting of mongodb services when server is powered on
systemctl start mongod
systemctl enable mongod
service mongod start

# downloading of our code repository
wget -c https://www.dropbox.com/s/6g4zfii8f0d7yny/bookreviews.zip?dl=0 -O bookreviews.zip
apt-get install -y unzip
unzip bookreviews.zip -d "/home/ubuntu/bookreviews"

# run script to generate new metadata
apt-get install -y python3-pip # install pip3 for merge_cover_texts.py
yes | pip3 install fire # install dependencies for merge_cover_texts.py

home="/home/ubuntu"
sudo chown -R ubuntu:ubuntu $home/bookreviews
chmod +x $home/bookreviews/boto3/bash_scripts/get_data.sh
source $home/bookreviews/boto3/bash_scripts/get_data.sh

# run script to merge data
python3 /home/ubuntu/bookreviews/boto3/bash_scripts/mongodb/merge_cover_texts.py --meta_json="/home/ubuntu/bookreviews/data_store/meta_Kindle_Store.json" --texts_csv="/home/ubuntu/bookreviews/extra_data/kindle_cover_texts.csv" --output_json="/home/ubuntu/bookreviews/data_store/meta_new.json"

# importing dataset
mongoimport --db 50043_db --collection books_metadata --file /home/ubuntu/bookreviews/data_store/meta_new.json --legacy

# replacing default config files
yes | sudo rm /etc/mongod.conf
mv $home/bookreviews/boto3/config_files/mongod.conf /etc/
chown -R root:root /etc/mongod.conf # give back root permissions to the config file
chmod 644 /etc/mongod.conf