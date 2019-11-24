#!/bin/bash
scriptdir="$(dirname "$0")"
cd "$scriptdir"

# import variables server_ip, public_key, username
source ../../config_files/config_mysql.sh

# check if there is a command line argument
if [ $# -eq 0 ]
    then
    echo "No url specified. Using default dropbox url"
    dropbox_url=https://www.dropbox.com/s/6g4zfii8f0d7yny/bookreviews.zip?dl=0
else
    dropbox_url=$1
fi

# scp datasets to folder in ec2 instance
scp -o StrictHostKeyChecking=no -i ~/.ssh/$public_key ../get_data.sh $username@$server_ip:/home/$username
ssh -o StrictHostKeyChecking=no -i ~/.ssh/$public_key $username@$server_ip 'sudo apt-get -y install unzip'
ssh -o StrictHostKeyChecking=no -i ~/.ssh/$public_key $username@$server_ip './get_data.sh'

# scp scripts to folder in ec2 instance
echo "Transferring scripts to EC2 instance"
scp -o StrictHostKeyChecking=no -i ~/.ssh/$public_key initialize_mysql.sql $username@$server_ip:/home/$username
scp -o StrictHostKeyChecking=no -i ~/.ssh/$public_key mysql_setup.sh $username@$server_ip:/home/$username

# scp config file into server
echo "copying over config file"
scp -o StrictHostKeyChecking=no -i ~/.ssh/$public_key ../../config_files/mysqld.cnf $username@$server_ip:/etc/mysql/mysql.conf.d/

# run scripts in ec2 instance

# grant user permission to root, setup database and users
ssh -o StrictHostKeyChecking=no -i ~/.ssh/$public_key $username@$server_ip "sudo ./mysql_setup.sh ${dropbox_url}"
# create tables and import data
echo "Importing data to MySQL"
ssh -o StrictHostKeyChecking=no -i ~/.ssh/$public_key $username@$server_ip 'sudo mysql -u root < initialize_mysql.sql'