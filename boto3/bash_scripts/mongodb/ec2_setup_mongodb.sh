#!/bin/bash

# import server_ip, username, public_key variables
source ../config/config_mongodb.sh

# check for command line arguments
if [ $# -eq 0 ]
    then
    echo "No url specified. Using default dropbox url"
    dropbox_url=https://www.dropbox.com/s/6g4zfii8f0d7yny/bookreviews.zip?dl=0
else
    dropbox_url=$1
fi

# add fingerprint of server to known hosts
echo "adding mongodb server ($server_ip) to known_hosts"
ssh-keygen -R $server_ip
ssh-keyscan -t ecdsa -H $server_ip >> ~/.ssh/known_hosts

# replace mongodb config file that with bind 0.0.0.0
scp -i ~/.ssh/$public_key ../config/mongod.conf $username@$server_ip:/home/$username

# copy over create_user script
scp -i ~/.ssh/$public_key ../mongodb/create_user.js $username@$server_ip:/home/$username

# copy over scripts to import dataset to server
scp -i ~/.ssh/$public_key ../../get_data.sh $username@$server_ip:/home/$username
ssh -i ~/.ssh/$public_key $username@$server_ip 'sudo apt-get -y install unzip'
ssh -i ~/.ssh/$public_key $username@$server_ip './get_data.sh'

# copy scripts to server and execute them on server
scp -i ~/.ssh/$public_key ../mongodb/mongodb_setup.sh $username@$server_ip:/home/$username
ssh -i ~/.ssh/$public_key $username@$server_ip "./mongodb_setup.sh ${dropbox_url}"