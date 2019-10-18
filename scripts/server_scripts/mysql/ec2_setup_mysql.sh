#!/bin/bash

# run this script as sudo to avoid constant prompts
# this script runs on our local machine and sets up the server
server_ip="13.58.54.227"
private_key="experimental_instance.pem"
username="ubuntu"

# scp datasets to folder in ec2 instance
# scp -i ~/.ssh/experimental_instance.pem ../../data_store/kindle_reviews.csv ubuntu@$server_ip:/home/ubuntu # takes a really long time

scp -i ~/.ssh/$private_key ../../get_data.sh $username@$server_ip:/home/$username
ssh -i ~/.ssh/$private_key $username@$server_ip 'sudo apt-get -y install unzip' # install unzip to unzip data from get_data.sh
ssh -i ~/.ssh/$private_key $username@$server_ip './get_data.sh' # might be faster to just unzip the data, but needs unzip

# scp scripts to folder in ec2 instance
scp -i ~/.ssh/$private_key initialize_mysql.sql $username@$server_ip:/home/$username
scp -i ~/.ssh/$private_key mysql_setup.sh $username@$server_ip:/home/$username

# run scripts in ec2 instance
ssh -i ~/.ssh/$private_key $username@$server_ip 'sudo ./mysql_setup.sh'