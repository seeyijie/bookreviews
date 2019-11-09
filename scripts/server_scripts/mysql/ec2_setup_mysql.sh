#!/bin/bash

# run this script as sudo to avoid constant prompts
# this script runs on our local machine and sets up the server
server_ip="52.14.103.65"
public_key="experimental_instance.pem"
username="ubuntu"
if [ $# -eq 0 ]
    then
    echo "No url specified. Using default dropbox url"
    dropbox_url=https://www.dropbox.com/s/6g4zfii8f0d7yny/bookreviews.zip?dl=0
else
    dropbox_url=$1
fi

# scp datasets to folder in ec2 instance
scp -i ~/.ssh/$public_key ../../get_data.sh $username@$server_ip:/home/$username
ssh -i ~/.ssh/$public_key $username@$server_ip 'sudo apt-get -y install unzip'
ssh -i ~/.ssh/$public_key $username@$server_ip './get_data.sh'

# scp scripts to folder in ec2 instance
scp -i ~/.ssh/$public_key initialize_mysql.sql $username@$server_ip:/home/$username
scp -i ~/.ssh/$public_key mysql_setup.sh $username@$server_ip:/home/$username

# run scripts in ec2 instance

# grant user permission to root, setup database and users
ssh -i ~/.ssh/$public_key $username@$server_ip "sudo ./mysql_setup.sh ${dropbox_url}"
# create tables and import data
echo "Importing data to MySQL"
ssh -i ~/.ssh/$public_key $username@$server_ip 'sudo mysql -u root < initialize_mysql.sql'