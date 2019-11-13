#!/bin/bash

source ../config/config_mongodb.sh

if [ $# -eq 0 ]
    then
    echo "No url specified. Using default dropbox url"
    dropbox_url=https://www.dropbox.com/s/6g4zfii8f0d7yny/bookreviews.zip?dl=0
else
    dropbox_url=$1
fi

echo "adding mongodb server ($server_ip) to known_hosts"
ssh-keygen -R $server_ip
ssh-keyscan -t ecdsa -H $server_ip >> ~/.ssh/known_hosts

# scp datasets to folder in ec2 instance
scp -i ~/.ssh/$public_key ../../get_data.sh $username@$server_ip:/home/$username
ssh -i ~/.ssh/$public_key $username@$server_ip 'sudo apt-get -y install unzip'
ssh -i ~/.ssh/$public_key $username@$server_ip './get_data.sh'

# scp scripts to folder in ec2 instance
scp -i ~/.ssh/$public_key ../mongodb/mongodb_setup.sh $username@$server_ip:/home/$username
ssh -i ~/.ssh/$public_key $username@$server_ip "./mongodb_setup.sh ${dropbox_url}"
