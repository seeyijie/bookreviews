#!/bin/bash

source ../config/config_mysql.sh

if [ $# -eq 0 ]
    then
    echo "No url specified. Using default dropbox url"
    dropbox_url=https://www.dropbox.com/s/6g4zfii8f0d7yny/bookreviews.zip?dl=0
else
    dropbox_url=$1
fi

echo "adding mysql server ($server_ip) to known_hosts"
ssh-keygen -R $server_ip
ssh-keyscan -t ecdsa -H $server_ip >> ~/.ssh/known_hosts

# scp datasets to folder in ec2 instance
scp -i ~/.ssh/$public_key ../../get_data.sh $username@$server_ip:/home/$username
ssh -i ~/.ssh/$public_key $username@$server_ip 'sudo apt-get -y install unzip'
ssh -i ~/.ssh/$public_key $username@$server_ip './get_data.sh'

# scp scripts to folder in ec2 instance
echo "Transferring scripts to EC2 instance"
scp -i ~/.ssh/$public_key ../mysql/initialize_mysql.sql $username@$server_ip:/home/$username
scp -i ~/.ssh/$public_key ../mysql/mysql_setup.sh $username@$server_ip:/home/$username

# run scripts in ec2 instance

# grant user permission to root, setup database and users
ssh -i ~/.ssh/$public_key $username@$server_ip "sudo ./mysql_setup.sh ${dropbox_url}"
# create tables and import data
echo "Importing data to MySQL"
ssh -i ~/.ssh/$public_key $username@$server_ip 'sudo mysql -u root < initialize_mysql.sql'