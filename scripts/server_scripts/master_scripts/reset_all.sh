#!/bin/bash

# TODO: Running the script with sudo permissions uses /root/.ssh instead of using /home/user/.ssh. Find a way to fix this.
# clear all non hidden files in mysql server
source ../config/config_mysql.sh
su -c "ssh-keygen -R $server_ip" $USER 
su -c "ssh-keyscan -H $server_ip >> ~/.ssh/known_hosts" $USER

ssh -i ~/.ssh/$public_key $username@$server_ip "sudo rm -rf /home/ubuntu/*"
su -c "ssh-keygen -R $server_ip" $USER

# clear all non hidden files in mongodb server
# source ../config/config_mongodb.sh
# sudo -u $USER ssh-keygen -R $server_ip
# sudo -u $USER ssh-keyscan -H $server_ip >> ~/.ssh/known_hosts

# ssh -i ~/.ssh/$public_key $username@$server_ip "sudo rm -rf /home/ubuntu/*"
# sudo -u $USER ssh-keygen -R $server_ip

# clear all non hidden files in flask server
# source ../config/flask.sh
# ssh-keygen -R $server_ip
# ssh-keyscan -H $server_ip >> /root/.ssh/known_hosts
# ssh-keygen -R $server_ip

# ssh -i ~/.ssh/$public_key $username@$server_ip "sudo rm -rf /home/ubuntu/*"