#!/bin/bash

# run this script as sudo to avoid constant prompts
# this script runs on our local machine and sets up the server
server_ip="3.18.111.43"
public_key="experimental_instance.pem"
username="ubuntu"

# scp datasets to folder in ec2 instance
scp -i ~/.ssh/$public_key ../../get_data.sh $username@$server_ip:/home/$username
ssh -i ~/.ssh/$public_key $username@$server_ip 'sudo apt-get -y install unzip'
ssh -i ~/.ssh/$public_key $username@$server_ip './get_data.sh'

# scp scripts to folder in ec2 instance
scp -i ~/.ssh/$public_key initialize_mysql.sql $username@$server_ip:/home/$username
scp -i ~/.ssh/$public_key mysql_setup.sh $username@$server_ip:/home/$username

# run scripts in ec2 instance

# grant user permission to root, setup database and users
ssh -i ~/.ssh/$public_key $username@$server_ip 'sudo ./mysql_setup.sh'
# create tables and import data
echo "Importing data to MySQL"
ssh -i ~/.ssh/$public_key $username@$server_ip 'sudo mysql -u root < initialize_mysql.sql'