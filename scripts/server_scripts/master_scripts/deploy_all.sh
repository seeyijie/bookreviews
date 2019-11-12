#!/bin/bash

if [ "$EUID" -eq 0 ] # Root has $EUID = 0
  then echo "Please run this script as non-root (no sudo)."
  exit
fi

# sequential deployment of servers on EC2. (Next step: aim to parallelize)
if [ $# -eq 0 ]
    then
    echo "No url specified. Using default dropbox url"
    dropbox_url=https://www.dropbox.com/s/6g4zfii8f0d7yny/bookreviews.zip?dl=0
else
    dropbox_url=$1
fi

source ../config/config_mysql.sh
echo "adding mysql server ($server_ip) to known_hosts"
ssh-keygen -R $server_ip
ssh-keyscan -t ecdsa -H $server_ip >> ~/.ssh/known_hosts
# ssh-keyscan -t ecdsa -H 3.16.187.168 >> ~/.ssh/known_hosts

source ../config/config_flask.sh
echo "adding flask server ($server_ip) fingerprint to known_hosts"
ssh-keygen -R $server_ip
ssh-keyscan -t ecdsa -H $server_ip >> ~/.ssh/known_hosts

source ../config/config_mongodb.sh
echo "adding mongodb server ($server_ip) fingerprint to known_hosts"
ssh-keygen -R $server_ip
ssh-keyscan -t ecdsa -H $server_ip >> ~/.ssh/known_hosts

# deployment of MongoDB server
# echo "************ Deploying MongoDB server **************"
# sudo ./../mongodb/ec2_setup_mongodb.sh ${dropbox_url}

# deployment of MySQL server
echo "************ Deploying MySQL server **************"
sudo ./../mysql/ec2_setup_mysql.sh ${dropbox_url}

# deployment of Flask server
# echo "************ Deploying Flask server **************"
# sudo ./../flask/ec2_setup_flask.sh ${dropbox_url}
# wait
echo "deployment of Servers completed"

# TODO: add "&" to run deployment in background. Prerequisite, remove everything from home folder before doing installation otherwise we will not be able to answer prompts when processes are in background
